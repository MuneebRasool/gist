from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "emails" (
    "id" UUID NOT NULL PRIMARY KEY,
    "message_id" VARCHAR(255) NOT NULL UNIQUE,
    "body" TEXT NOT NULL,
    "subject" VARCHAR(255),
    "from_" VARCHAR(255),
    "snippet" VARCHAR(255),
    "date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "to" VARCHAR(255),
    "classification" VARCHAR(10) NOT NULL DEFAULT 'drawer',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "emails"."body" IS 'Email body content';
COMMENT ON TABLE "emails" IS 'EmailModel to store email data in PostgreSQL database.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "emails";"""
