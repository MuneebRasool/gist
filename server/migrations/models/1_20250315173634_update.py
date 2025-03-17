from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_models" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "utility_model" BYTEA,
    "cost_model" BYTEA,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_models_user_id_a64e1f" UNIQUE ("user_id")
);
COMMENT ON COLUMN "user_models"."utility_model" IS 'Serialized utility SGDRegressor model';
COMMENT ON COLUMN "user_models"."cost_model" IS 'Serialized cost SGDRegressor model';
COMMENT ON TABLE "user_models" IS 'UserModel model that represents the user_models table in the database.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_models";"""
