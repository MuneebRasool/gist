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
    "task_gen" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."nylas_grant_id" IS 'Encrypted Nylas grant ID';
COMMENT ON TABLE "users" IS 'User model that represents the users table in the database.';
CREATE TABLE IF NOT EXISTS "emails" (
    "id" UUID NOT NULL PRIMARY KEY,
    "message_id" VARCHAR(255) NOT NULL UNIQUE,
    "body" TEXT NOT NULL,
    "subject" VARCHAR(255),
    "from_" VARCHAR(255),
    "date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "emails"."body" IS 'Email body content';
COMMENT ON TABLE "emails" IS 'EmailModel to store email data in PostgreSQL database.';
CREATE TABLE IF NOT EXISTS "features" (
    "id" UUID NOT NULL PRIMARY KEY,
    "task_id" VARCHAR(255) NOT NULL,
    "features" JSONB NOT NULL,
    "cost" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "features" IS 'Features model that represents the features table in the database.';
CREATE TABLE IF NOT EXISTS "user_models" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "utility_model" BYTEA,
    "cost_model" BYTEA,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user_models"."utility_model" IS 'Serialized utility SGDRegressor model';
COMMENT ON COLUMN "user_models"."cost_model" IS 'Serialized cost SGDRegressor model';
COMMENT ON TABLE "user_models" IS 'UserModel model that represents the user_models table in the database.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
