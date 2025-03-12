from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "task_utility_features" (
            "id" UUID NOT NULL PRIMARY KEY,
            "priority" VARCHAR(50),
            "deadline_time" VARCHAR(100),
            "intrinsic_interest" VARCHAR(50),
            "user_personalization" VARCHAR(50),
            "task_type_relevance" VARCHAR(50),
            "emotional_salience" VARCHAR(50),
            "user_feedback" VARCHAR(50),
            "domain_relevance" VARCHAR(50),
            "novel_task" VARCHAR(50),
            "reward_pathways" VARCHAR(50),
            "social_collaborative_signals" VARCHAR(50),
            "time_of_day_alignment" VARCHAR(50),
            "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "task_id" UUID NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
        );
        CREATE INDEX "idx_task_utility_features_task_id" ON "task_utility_features" ("task_id");

        CREATE TABLE IF NOT EXISTS "task_cost_features" (
            "id" UUID NOT NULL PRIMARY KEY,
            "task_complexity" VARCHAR(50),
            "spam_probability" VARCHAR(50),
            "time_required" DOUBLE PRECISION,
            "emotional_stress_factor" VARCHAR(50),
            "location_dependencies" VARCHAR(50),
            "key_friction_factors" TEXT,
            "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "task_id" UUID NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
        );
        CREATE INDEX "idx_task_cost_features_task_id" ON "task_cost_features" ("task_id");
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "task_utility_features";
        DROP TABLE IF EXISTS "task_cost_features";
        """
