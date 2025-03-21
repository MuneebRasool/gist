from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "emails" DROP COLUMN "to";
        ALTER TABLE "emails" DROP COLUMN "snippet";
        ALTER TABLE "emails" DROP COLUMN "classification";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "emails" ADD "to" VARCHAR(255);
        ALTER TABLE "emails" ADD "snippet" VARCHAR(255);
        ALTER TABLE "emails" ADD "classification" VARCHAR(10)NOT NULL DEFAULT 'drawer';"""
