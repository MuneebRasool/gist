from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tasks" (
            "id" UUID NOT NULL PRIMARY KEY,
            "task" VARCHAR(500) NOT NULL,
            "message_id" VARCHAR(255) NOT NULL,
            "priority" VARCHAR(50),
            "deadline" VARCHAR(100),
            "relevance_score" DOUBLE PRECISION,
            "utility_score" DOUBLE PRECISION,
            "cost_score" DOUBLE PRECISION,
            "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
        );
        CREATE INDEX "idx_tasks_user_id" ON "tasks" ("user_id");
        CREATE INDEX "idx_tasks_message_id" ON "tasks" ("message_id");
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "tasks";
        """
