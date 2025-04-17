from datetime import datetime, UTC
from typing import List, Optional, Dict, Any, Tuple
from src.models.graph.nodes import TaskNode, EmailNode, UserNode
from src.models.user import Features, User
from .schemas import TaskCreate, TaskUpdate
import uuid
from neomodel import db
from src.models.user import EmailModel


class TaskService:

    @staticmethod
    async def create_task(
        task_data: TaskCreate,
        user_id: str,
        utility_features: Optional[Dict[str, Any]] = None,
        cost_features: Optional[Dict[str, Any]] = None,
    ) -> TaskNode:
        """
        Create a new task and connect it to the corresponding email

        Args:
            task_data: Task data to create
            user_id: The ID of the user
            utility_features: Optional dictionary of utility features
            cost_features: Optional dictionary of cost features

        Returns:
            TaskNode: The created task node
        """
        # First get the email node
        email = TaskService.ensure_graph_nodes(user_id, task_data.messageId)

        # Create task node with classification included
        print("creating tasks")
        task = TaskNode(
            task_id=str(uuid.uuid4()),
            task=task_data.task,
            priority=task_data.priority,
            deadline=task_data.deadline if task_data.deadline else "No Deadline",
            utility_score=task_data.utility_score,
            cost_score=task_data.cost_score,
            relevance_score=task_data.relevance_score,
            classification=task_data.classification,
        ).save()

        # Connect task to email
        email.tasks.connect(task)
        task.messageId = task_data.messageId

        # Save features if provided
        if utility_features and cost_features:
            try:
                await Features.create_features(
                    user_id=user_id,
                    task_id=task.task_id,
                    utility_features=utility_features,
                    cost_features=cost_features,
                )
                print(f"Features saved for task {task.task_id}")
            except Exception as e:
                print(f"Error saving features for task {task.task_id}: {str(e)}")

        return task

    @staticmethod
    async def batch_create_tasks(
        task_data_list: List[TaskCreate],
        user_id: str,
        utility_features_list: Optional[List[Dict[str, Any]]] = None,
        cost_features_list: Optional[List[Dict[str, Any]]] = None,
        message_ids: Optional[List[str]] = None,
    ) -> List[TaskNode]:
        """
        Create multiple tasks at once and connect them to their respective emails

        Args:
            task_data_list: List of task data to create
            user_id: The ID of the user
            utility_features_list: Optional list of dictionaries containing utility features
            cost_features_list: Optional list of dictionaries containing cost features
            message_ids: Optional list of message IDs (if not included in TaskCreate objects)

        Returns:
            List[TaskNode]: The created task nodes
        """
        created_tasks = []

        # Validate input
        if message_ids and len(message_ids) != len(task_data_list):
            raise ValueError("message_ids must have the same length as task_data_list")

        if utility_features_list and len(utility_features_list) != len(task_data_list):
            raise ValueError(
                "utility_features_list must have the same length as task_data_list"
            )

        if cost_features_list and len(cost_features_list) != len(task_data_list):
            raise ValueError(
                "cost_features_list must have the same length as task_data_list"
            )

        # For each task, create the task and connect it to the email
        for i, task_data in enumerate(task_data_list):
            try:
                # Determine message ID
                message_id = message_ids[i] if message_ids else task_data.messageId

                # Get or create email node
                email = TaskService.ensure_graph_nodes(user_id, message_id)

                # Create task node
                task = TaskNode(
                    task_id=str(uuid.uuid4()),
                    task=task_data.task,
                    priority=task_data.priority,
                    deadline=(
                        task_data.deadline if task_data.deadline else "No Deadline"
                    ),
                    utility_score=task_data.utility_score,
                    cost_score=task_data.cost_score,
                    relevance_score=task_data.relevance_score,
                    classification=task_data.classification,
                ).save()

                # Connect task to email
                email.tasks.connect(task)
                task.messageId = message_id

                # Save features if provided
                if utility_features_list and cost_features_list:
                    try:
                        await Features.create_features(
                            user_id=user_id,
                            task_id=task.task_id,
                            utility_features=utility_features_list[i],
                            cost_features=cost_features_list[i],
                        )
                    except Exception as e:
                        print(
                            f"Error saving features for task {task.task_id}: {str(e)}"
                        )

                created_tasks.append(task)
            except Exception as e:
                print(f"Error creating task {i}: {str(e)}")
                # Continue with next task instead of failing the entire batch

        return created_tasks

    @staticmethod
    def ensure_graph_nodes(user_id: str, message_id: str) -> EmailNode:
        """
        Ensure User and Email nodes exist in the graph database
        Returns the EmailNode (creates if doesn't exist)
        """
        # Ensure user node exists
        try:
            user_node = UserNode.nodes.get(userid=str(user_id))
        except UserNode.DoesNotExist:
            user_node = UserNode(userid=user_id).save()

        # Ensure email node exists and is connected to user
        try:
            email_node = EmailNode.nodes.get(messageId=message_id)
        except EmailNode.DoesNotExist:
            email_node = EmailNode(messageId=message_id).save()
            user_node.emails.connect(email_node)

        return email_node

    @staticmethod
    async def get_task(task_id: str) -> Optional[TaskNode]:
        """Get a task by task_id"""
        try:
            task = TaskNode.nodes.get(task_id=task_id)
            return task
        except TaskNode.DoesNotExist:
            return None

    @staticmethod
    async def get_task_by_message_id(message_id: str) -> List[TaskNode]:
        """Get all tasks associated with a message ID"""
        query = """
        MATCH (e:EmailNode {messageId: $message_id})-[:CONTAINS_TASK]->(t:TaskNode)
        RETURN t
        """
        results, _ = db.cypher_query(query, {"message_id": message_id})
        return [TaskNode.inflate(row[0]) for row in results]

    @staticmethod
    async def get_tasks_by_user(user_id: str) -> List[TaskNode]:
        """Get all tasks for a specific user through the user->email->task relationship"""
        query = """
        MATCH (u:UserNode {userid: $user_id})-[:HAS_EMAIL]->(e:EmailNode)-[:CONTAINS_TASK]->(t:TaskNode)
        RETURN t
        ORDER BY t.relevance_score DESC
        """
        try:
            results, _ = db.cypher_query(query, {"user_id": user_id})
            return [TaskNode.inflate(row[0]) for row in results]
        except Exception as e:
            print(f"Error getting tasks for user {user_id}: {str(e)}")
            return []

    @staticmethod
    async def update_task(task_id: str, task_data: TaskUpdate) -> Optional[TaskNode]:
        """Update a task by task_id"""
        try:
            task = TaskNode.nodes.get(task_id=task_id)

            update_data = task_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(task, key, value)

            task.updatedAt = datetime.now(UTC)
            task.save()
            return task
        except TaskNode.DoesNotExist:
            return None

    @staticmethod
    async def delete_task(task_id: str) -> bool:
        """Delete a task by task_id"""
        try:
            task = TaskNode.nodes.get(task_id=task_id)
            # This will also remove all relationships
            task.delete()
            return True
        except TaskNode.DoesNotExist:
            return False

    @staticmethod
    async def add_task_dependency(task_id: str, depends_on_task_id: str) -> bool:
        """Add a dependency relationship between tasks"""
        try:
            task = TaskNode.nodes.get(task_id=task_id)
            depends_on_task = TaskNode.nodes.get(task_id=depends_on_task_id)

            task.depends_on.connect(depends_on_task)
            return True
        except TaskNode.DoesNotExist:
            return False

    @staticmethod
    async def get_task_dependencies(task_id: str) -> List[TaskNode]:
        """Get all tasks that this task depends on"""
        query = """
        MATCH (t:Task {task_id: $task_id})-[:DEPENDS_ON]->(d:Task)
        RETURN d
        """
        results, _ = db.cypher_query(query, {"task_id": task_id})
        return [TaskNode.inflate(row[0]) for row in results]

    @staticmethod
    async def get_task_features(task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get features for a task

        Args:
            task_id: The ID of the task

        Returns:
            Optional[Dict[str, Any]]: Dictionary containing utility and cost features if found, None otherwise
        """
        features = await Features.get_by_task_id(task_id)
        if not features:
            return None

        return {"utility_features": features.features, "cost_features": features.cost}

    @staticmethod
    async def get_user_emails(user_id: str) -> List[Dict[str, Any]]:
        """
        Get all emails for a specific user

        Args:
            user_id: The ID of the user

        Returns:
            List[Dict[str, Any]]: List of email nodes with their messageId
        """
        try:
            emails = await User.get_user_emails(user_id)
            # Map email.message_id to messageId as expected by EmailResponse schema
            return [{"messageId": email.message_id} for email in emails]
        except Exception as e:
            print(f"Error getting emails for user {user_id}: {str(e)}")
            return []

    @staticmethod
    async def get_emails_by_classification(
        user_id: str, classification: str
    ) -> List[Dict[str, Any]]:
        """
        Get all emails for a specific user with the specified classification in Neo4j

        Args:
            user_id: The ID of the user
            classification: The classification to filter by (e.g., "drawer", "library")

        Returns:
            List[Dict[str, Any]]: List of email nodes with the specified classification
        """
        query = """
        MATCH (u:UserNode {userid: $user_id})-[:HAS_EMAIL]->(e:EmailNode)
        WHERE e.classification = $classification
        RETURN e
        """
        try:
            results, _ = db.cypher_query(
                query, {"user_id": str(user_id), "classification": classification}
            )
            return [
                {
                    "messageId": row[0].get("messageId"),
                    "snippet": row[0].get("snippet"),
                    "subject": row[0].get("subject"),
                    "classification": row[0].get("classification"),
                }
                for row in results
            ]
        except Exception as e:
            print(f"Error getting {classification} emails for user {user_id}: {str(e)}")
            return []

    @staticmethod
    async def get_email_by_message_id(
        message_id: str, user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get a single email from Postgres Email model based on message_id

        Args:
            message_id: The message ID of the email
            user_id: Optional user ID to filter by (for security)

        Returns:
            Optional[Dict[str, Any]]: Email data if found, None otherwise
        """

        try:
            if user_id:
                email = await EmailModel.get_by_message_id(message_id, user_id)

            return {
                "id": str(email.id),
                "messageId": email.message_id,
                "subject": email.subject,
                "body": email.body,
                "from": email.from_,
                "date": email.date.isoformat() if email.date else None,
            }
        except Exception as e:
            print(f"Error getting email with message ID {message_id}: {str(e)}")
            return None
