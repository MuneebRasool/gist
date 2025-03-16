from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_user_models_user_id_a64e1f";
        ALTER TABLE "user_models" DROP CONSTRAINT IF EXISTS "fk_user_mod_users_d4d4212f";
        ALTER TABLE "user_models" ADD CONSTRAINT "fk_user_mod_users_d4d4212f" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX "uid_user_models_user_id_a64e1f" ON "user_models" ("user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_user_models_user_id_a64e1f";
        ALTER TABLE "user_models" DROP CONSTRAINT IF EXISTS "fk_user_mod_users_d4d4212f";
        ALTER TABLE "user_models" ADD CONSTRAINT "fk_user_mod_users_d4d4212f" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX "uid_user_models_user_id_a64e1f" ON "user_models" ("user_id");"""
