from tortoise import fields, models
import bcrypt
from src.utils.encryption import encryption
from io import BytesIO
import joblib
from sklearn.linear_model import SGDRegressor
import numpy as np
import uuid
from typing import Optional, List


class User(models.Model):
    """
    User model that represents the users table in the database.
    """

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    avatar = fields.CharField(max_length=255, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    is_active = fields.BooleanField(default=True)
    verified = fields.BooleanField(default=False)
    verification_code = fields.CharField(max_length=6, null=True)
    verification_code_expires_at = fields.DatetimeField(null=True)
    personality = fields.JSONField(null=True, default=list)
    nylas_email = fields.CharField(max_length=255, null=True)
    nylas_grant_id = fields.TextField(null=True, description="Encrypted Nylas grant ID")
    onboarding = fields.BooleanField(default=False)
    domain_inf = fields.CharField(max_length=255, null=True)
    task_gen = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # One-to-One Relation with UserModel
    user_model: fields.OneToOneRelation["UserModel"]

    async def set_nylas_grant_id(self, grant_id: str) -> None:
        """Encrypt and store Nylas grant ID."""
        if grant_id:
            self.nylas_grant_id = encryption.encrypt(grant_id)

    def get_nylas_grant_id(self) -> str | None:
        """Decrypt and return Nylas grant ID."""
        return encryption.decrypt(self.nylas_grant_id) if self.nylas_grant_id else None

    async def get_all_users_by_grant_id(self, grant_id: str):
        users = await User.filter(nylas_grant_id__not_isnull=True).all()
        return [user for user in users if user.get_nylas_grant_id() == grant_id]

    def verify_password(self, password: str) -> bool:
        """Verify a password against its hash."""
        return (
            bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))
            if self.password_hash
            else False
        )

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    async def get_by_grant_id(grant_id: str):
        """Get user by Nylas grant ID."""
        users = await User.filter(nylas_grant_id__not_isnull=True).all()
        return next(
            (user for user in users if user.get_nylas_grant_id() == grant_id), None
        )

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"

    class PydanticMeta:
        exclude = ["password_hash"]


class UserModel(models.Model):
    """
    UserModel model that represents the user_models table in the database.
    Stores serialized SGDRegressor models for utility and cost predictions.
    """

    user = fields.OneToOneField(
        "models.User", related_name="user_model", on_delete=fields.CASCADE
    )
    utility_model = fields.BinaryField(
        null=True, description="Serialized utility SGDRegressor model"
    )
    cost_model = fields.BinaryField(
        null=True, description="Serialized cost SGDRegressor model"
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_models"

    def __str__(self):
        # Use self.user.id directly instead of user_id property
        return f"Models for User {self.user.id}"

    # Serialization/Deserialization Helpers
    @staticmethod
    def _serialize_model(model) -> bytes:
        """Serialize an SGDRegressor model to bytes."""
        buffer = BytesIO()
        joblib.dump(model, buffer)

        return buffer.getvalue()

    @staticmethod
    def _deserialize_model(model_bytes: bytes) -> SGDRegressor:
        """Deserialize bytes back into an SGDRegressor model."""
        if not model_bytes:
            # Create a default model and ensure it's fitted with minimal data
            model = SGDRegressor()
            model.fit(np.array([[0.5]]), np.array([0.5]))  # Fit with minimal data
            return model
        buffer = BytesIO(model_bytes)
        return joblib.load(buffer)

    # Instance Methods
    async def get_utility_model(self) -> SGDRegressor:
        """Retrieve and deserialize the utility model."""
        return self._deserialize_model(self.utility_model)

    async def get_cost_model(self) -> SGDRegressor:
        """Retrieve and deserialize the cost model."""
        return self._deserialize_model(self.cost_model)

    async def set_models(
        self, utility_model: SGDRegressor, cost_model: SGDRegressor
    ) -> None:
        """Serialize and set the utility and cost models."""
        if not hasattr(utility_model, "coef_"):
            utility_model.fit(np.array([[0.5]]), np.array([0.5]))
        if not hasattr(cost_model, "coef_"):
            cost_model.fit(np.array([[0.5]]), np.array([0.5]))

        self.utility_model = self._serialize_model(utility_model)
        self.cost_model = self._serialize_model(cost_model)
        await self.save()

    @classmethod
    async def get_or_create(cls, user_id: str) -> "UserModel":
        """Get or create a UserModel instance."""
        user = await User.get(id=user_id)
        existing_model = await cls.filter(user=user).first()
        if existing_model:
            return existing_model
        new_model = await cls.create(user=user)
        return new_model


class EmailModel(models.Model):
    """
    EmailModel to store email data in PostgreSQL database.
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField(
        "models.User", related_name="emails", on_delete=fields.CASCADE
    )
    message_id = fields.CharField(max_length=255, unique=True)
    body = fields.TextField(description="Email body content")
    subject = fields.CharField(max_length=255, null=True)
    from_ = fields.CharField(max_length=255, null=True)
    date = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "emails"

    def __str__(self):
        return f"Email {self.message_id} ({self.subject})"

    @classmethod
    async def get_by_message_id(cls, message_id: str) -> Optional["EmailModel"]:
        """
        Get email by message ID

        Args:
            message_id: The ID of the email message

        Returns:
            Optional[EmailModel]: The email record if found, None otherwise
        """
        return await cls.filter(message_id=message_id).first()

    @classmethod
    async def create_email(cls, user_id: str, email_data: dict) -> "EmailModel":
        """
        Create a new email record

        Args:
            user_id: The ID of the user
            email_data: Dictionary containing email data

        Returns:
            EmailModel: The created email record
        """
        try:
            user = await User.get(id=user_id)

            # Extract values with defaults for optional fields
            message_id = email_data.get("id", "")
            body = email_data.get("body", "")
            subject = email_data.get("subject", None)

            # Handle from_ which could be a list of dicts or a string
            from_data = email_data.get("from", [])
            from_str = ""

            if isinstance(from_data, list) and len(from_data) > 0:
                if isinstance(from_data[0], dict):
                    # Extract name and email if available
                    name = from_data[0].get("name", "")
                    email = from_data[0].get("email", "")
                    from_str = f"{name} <{email}>" if name else email
                else:
                    from_str = str(from_data[0])
            elif isinstance(from_data, str):
                from_str = from_data

            # Create the email record
            email = await cls.create(
                id=uuid.uuid4(),
                user=user,
                message_id=message_id,
                body=body,
                subject=subject,
                from_=from_str,
            )

            return email
        except Exception as e:
            print(f"Error creating email record: {str(e)}")
            raise

    @classmethod
    async def batch_create_emails(
        cls, user_id: str, email_data_list: List[dict]
    ) -> List["EmailModel"]:
        """
        Create multiple email records in a single batch operation

        Args:
            user_id: The ID of the user
            email_data_list: List of dictionaries containing email data

        Returns:
            List[EmailModel]: The created email records
        """
        try:
            if not email_data_list:
                return []

            user = await User.get(id=user_id)

            # Prepare all email models
            email_models = []
            for email_data in email_data_list:
                # Skip if no message_id (required field)
                if not email_data.get("id"):
                    continue

                # Handle from_ which could be a list of dicts or a string
                from_data = email_data.get("from", [])
                from_str = ""

                if isinstance(from_data, list) and len(from_data) > 0:
                    if isinstance(from_data[0], dict):
                        # Extract name and email if available
                        name = from_data[0].get("name", "")
                        email = from_data[0].get("email", "")
                        from_str = f"{name} <{email}>" if name else email
                    else:
                        from_str = str(from_data[0])
                elif isinstance(from_data, str):
                    from_str = from_data

                # Create email model instance (not saved yet)
                email_models.append(
                    cls(
                        id=uuid.uuid4(),
                        user=user,
                        message_id=email_data.get("id", ""),
                        body=email_data.get("body", ""),
                        subject=email_data.get("subject", None),
                        from_=from_str,
                    )
                )

            # Save all emails in a batch operation
            if email_models:
                try:
                    created_emails = await cls.bulk_create(email_models)
                    return created_emails if created_emails else []
                except Exception as e:
                    print(f"Error in bulk create: {str(e)}")
                    # Fallback to individual creation
                    created_emails = []
                    for model in email_models:
                        try:
                            await model.save()
                            created_emails.append(model)
                        except Exception as individual_e:
                            print(
                                f"Error saving individual email {model.message_id}: {str(individual_e)}"
                            )
                    return created_emails

            return []

        except Exception as e:
            print(f"Error batch creating email records: {str(e)}")
            return []

    @classmethod
    async def get_user_emails(cls, user_id: str) -> List["EmailModel"]:
        """
        Get all emails for a specific user

        Args:
            user_id: The ID of the user

        Returns:
            List[EmailModel]: List of email records for the user
        """
        try:
            user = await User.get(id=user_id)
            emails = await cls.filter(user=user).all()
            return emails
        except Exception as e:
            print(f"Error getting user emails: {str(e)}")
            return []


class Features(models.Model):
    """
    Features model that represents the features table in the database.
    Stores extracted utility and cost features for each task.
    """

    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="features", on_delete=fields.CASCADE
    )
    task_id = fields.CharField(max_length=255)
    features = fields.JSONField()
    cost = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "features"

    def __str__(self):
        return f"Features for Task {self.task_id} ({self.user.email})"

    @classmethod
    async def create_features(
        cls, user_id: str, task_id: str, utility_features: dict, cost_features: dict
    ) -> "Features":
        """
        Create a new features record for a task

        Args:
            user_id: The ID of the user
            task_id: The ID of the task
            utility_features: Dictionary of utility features
            cost_features: Dictionary of cost features

        Returns:
            Features: The created features record
        """
        user = await User.get(id=user_id)

        features = await cls.create(
            id=uuid.uuid4(),
            user=user,
            task_id=task_id,
            features=utility_features,
            cost=cost_features,
        )

        return features

    @classmethod
    async def get_by_task_id(cls, task_id: str) -> Optional["Features"]:
        """
        Get features by task ID

        Args:
            task_id: The ID of the task

        Returns:
            Optional[Features]: The features record if found, None otherwise
        """
        return await cls.filter(task_id=task_id).first()

    @classmethod
    async def get_by_user_id(cls, user_id: str) -> List["Features"]:
        """
        Get all features for a user

        Args:
            user_id: The ID of the user

        Returns:
            List[Features]: List of features records for the user
        """
        user = await User.get(id=user_id)
        return await cls.filter(user=user).all()
