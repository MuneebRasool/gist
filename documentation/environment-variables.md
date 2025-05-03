# Environment Variables

This document lists the key environment variables for Gist.

## Frontend Variables

```env
NEXTAUTH_SECRET="super-secret"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_APP_URL="http://localhost:3000"   # for local development
NEXT_PUBLIC_API_URL="http://localhost:8000"   # for local development

# Google OAuth
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

# Environment
ENV=development
DEBUG=True
```

* `NEXTAUTH_SECRET`: Secret for NextAuth session
* `NEXTAUTH_URL`: App base URL
* `NEXT_PUBLIC_APP_URL`: Frontend URL
* `NEXT_PUBLIC_API_URL`: Backend API URL
* Google OAuth keys: set from Google Cloud Console

## Backend Variables

```env
ENV=development
DEBUG=True

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=db_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

SECRET_KEY=your-super-duper-secret-key

API_V1_PREFIX=/api

ALLOWED_HOSTS=["*"]

LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY="api key"

NYLAS_API_URI=https://api.us.nylas.com
NYLAS_CALLBACK_URI=http://localhost:3000/oauth/exchange

NYLAS_CLIENT_ID="client id"
NYLAS_API_KEY="api key"

LANGFUSE_PUBLIC_KEY="get it from langfuse dashboard"
LANGFUSE_SECRET_KEY="get it from langfuse dashboard"
LANGFUSE_HOST="https://cloud.langfuse.com"

```
