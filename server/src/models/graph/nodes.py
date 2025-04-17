from neomodel import (
    StructuredNode,
    StringProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
    One,
    ZeroOrMore,
    OneOrMore,
    FloatProperty,
)
from datetime import datetime, UTC


class UserNode(StructuredNode):
    """
    User node that represents a user in the graph database.
    Only stores userid as reference since actual user data is in PostgreSQL.
    """

    userid = StringProperty(unique_index=True, required=True)
    emails = RelationshipTo("EmailNode", "HAS_EMAIL", cardinality=ZeroOrMore)


class EmailNode(StructuredNode):
    """
    Email node that represents an email in the graph database.
    References email by its ID since actual email data is stored elsewhere.
    """

    messageId = StringProperty(required=True)
    snippet = StringProperty(default=None)
    subject = StringProperty(default=None)
    classification = StringProperty(default=None)
    tasks = RelationshipTo("TaskNode", "CONTAINS_TASK", cardinality=ZeroOrMore)
    user = RelationshipFrom("UserNode", "HAS_EMAIL", cardinality=OneOrMore)


class TaskNode(StructuredNode):
    """
    Task node that represents a task extracted from emails.
    """

    task_id = StringProperty(unique_index=True, required=True)
    task = StringProperty(required=True)
    deadline = StringProperty(default=None)
    priority = StringProperty(default=None)
    relevance_score = FloatProperty(default=0.0)
    utility_score = FloatProperty(default=0.0)
    cost_score = FloatProperty(default=0.0)
    classification = StringProperty(default=None)
    createdAt = DateTimeProperty(default=lambda: datetime.now(UTC))
    updatedAt = DateTimeProperty(default=lambda: datetime.now(UTC))

    # Relationships
    email = RelationshipFrom("EmailNode", "CONTAINS_TASK", cardinality=One)
    depends_on = RelationshipTo("TaskNode", "DEPENDS_ON", cardinality=ZeroOrMore)
