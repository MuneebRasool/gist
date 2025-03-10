from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "avatar" VARCHAR(255),
    "password_hash" VARCHAR(128),
    "is_active" BOOL NOT NULL DEFAULT True,
    "verified" BOOL NOT NULL DEFAULT False,
    "verification_code" VARCHAR(6),
    "verification_code_expires_at" TIMESTAMPTZ,
    "personality" JSONB,
    "nylas_email" VARCHAR(255),
    "nylas_grant_id" TEXT,
    "onboarding" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."nylas_grant_id" IS 'Encrypted Nylas grant ID';
COMMENT ON TABLE "users" IS 'User model that represents the users table in the database.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
