# Environment Variables Documentation

This document provides detailed information about all environment variables used in the GIST project, clearly separated between frontend and backend requirements.

## Table of Contents
- [Frontend Environment Variables](#frontend-environment-variables)
- [Backend Environment Variables](#backend-environment-variables)
- [Environment Setup Steps](#environment-setup-steps)
- [Security Best Practices](#security-best-practices)

## Frontend Environment Variables

### Authentication & OAuth
```
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

### NextAuth Configuration
- `NEXTAUTH_SECRET`: A secret key used for NextAuth.js session encryption
  - Generate using: `openssl rand -base64 32`
  - Keep this secret and never commit it to version control
- `NEXTAUTH_URL`: The base URL of your application
  - Development: `http://localhost:3000`
  - Production: Your production domain
- `NEXT_PUBLIC_APP_URL`: Public URL for your frontend application
- `NEXT_PUBLIC_API_URL`: Public URL for your backend API

### Google OAuth
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret

To obtain Google OAuth credentials:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth client ID"
5. Select "Web application"
6. Add authorized redirect URIs:
   - Development: `http://localhost:3000/api/auth/callback/google`
   - Production: `https://your-domain.com/api/auth/callback/google`
7. Copy the generated Client ID and Client Secret

## Backend Environment Variables

```
# Environment
ENV=development
DEBUG=True

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=db_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Security
SECRET_KEY=your-super-duper-secret-key

# API
API_V1_PREFIX=/api

# CORS
ALLOWED_HOSTS=["*"]  # In production, replace with specific origins

# LLM Configuration
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY="api key"

# Nylas Configuration
NYLAS_API_URI=https://api.us.nylas.com
NYLAS_CALLBACK_URI=http://localhost:3000/oauth/exchange    # for local development
NYLAS_CLIENT_ID="client id"
NYLAS_API_KEY="api key"

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY="get it from langfuse dashboard"
LANGFUSE_SECRET_KEY="get it from langfuse dashboard"
LANGFUSE_HOST="https://cloud.langfuse.com"
```

### Database Configuration

#### PostgreSQL
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `POSTGRES_HOST`: Database host address
- `POSTGRES_PORT`: Database port (default: 5432)
- `DATABASE_URL`: Full PostgreSQL connection string
  - Format: `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}`

To set up PostgreSQL:
1. Install PostgreSQL locally or use a cloud provider (e.g., AWS RDS, Supabase, Neon)
2. Create a new database and user
3. Note down the credentials and connection details

### Neo4j Configuration

- `NEO4J_URI`: Neo4j database connection URI
- `NEO4J_USERNAME`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password

To set up Neo4j:
1. Sign up for [Neo4j Aura](https://neo4j.com/cloud/platform/aura-graph-database/) or install locally
2. Create a new database instance
3. Note down the connection details and credentials

### API Configuration

- `API_V1_PREFIX`: API version prefix (default: `/api`)
- `SECRET_KEY`: Application secret key for encryption
  - Generate using: `openssl rand -base64 32`
- `ALLOWED_HOSTS`: List of allowed CORS origins
  - Development: `["*"]`
  - Production: `["https://your-domain.com"]`

### Nylas Configuration

- `NYLAS_CLIENT_ID`: Nylas API client ID
- `NYLAS_API_KEY`: Nylas API key
- `NYLAS_API_URI`: Nylas API endpoint
- `NYLAS_CALLBACK_URI`: OAuth callback URL

To obtain Nylas credentials:
1. Sign up for [Nylas](https://www.nylas.com/)
2. Create a new application
3. Configure OAuth settings with your callback URL
4. Note down the client ID and API key

### LLM Configuration

- `LLM_BASE_URL`: Base URL for LLM API
- `LLM_API_KEY`: API key for LLM service

To obtain OpenAI credentials:
1. Sign up for [OpenAI](https://platform.openai.com/)
2. Generate an API key in your account settings
3. Use the API key as `LLM_API_KEY`

### Langfuse Configuration

- `LANGFUSE_PUBLIC_KEY`: Public key for Langfuse API authentication
- `LANGFUSE_SECRET_KEY`: Secret key for Langfuse API authentication
- `LANGFUSE_HOST`: Host URL for Langfuse service (default: `https://cloud.langfuse.com`)

To obtain Langfuse credentials:
1. Sign up for [Langfuse](https://langfuse.com/)
2. Create a new project
3. Navigate to "API Keys" in your project settings
4. Copy the generated Public and Secret keys
5. Use these keys in your configuration

Langfuse is used for monitoring and observing LLM operations, helping with:
- Tracking token usage and costs
- Monitoring LLM performance metrics
- Debugging complex AI workflows
- Optimizing prompts and model selection

## Environment Setup Steps

1. Create two separate `.env` files:
   - `.env.local` for frontend (Next.js)
   - `.env` for backend
2. Fill in all required variables following the instructions above
3. For development:
   - Use localhost URLs
   - Set `ENV=development`
   - Set `DEBUG=True`
4. For production:
   - Use production URLs
   - Set `ENV=production`
   - Set `DEBUG=False`
   - Use secure values for all secrets
   - Configure proper CORS settings

## Security Best Practices

1. Never commit `.env` files to version control
2. Use strong, randomly generated secrets
3. Regularly rotate API keys and passwords
4. Use environment-specific configurations
5. Keep sensitive data encrypted
6. Use secure protocols (HTTPS) in production
7. Implement proper access controls for all services