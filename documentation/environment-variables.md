# Environment Variables Documentation

This document provides detailed information about all environment variables used in the GIST project, including how to obtain them and their purposes.

## Table of Contents
- [Authentication & OAuth](#authentication--oauth)
- [Database Configuration](#database-configuration)
- [Neo4j Configuration](#neo4j-configuration)
- [API Configuration](#api-configuration)
- [Email Configuration](#email-configuration)
- [Nylas Configuration](#nylas-configuration)
- [LLM Configuration](#llm-configuration)
- [LangChain Configuration](#langchain-configuration)

## Authentication & OAuth

### NextAuth Configuration
- `NEXTAUTH_SECRET`: A secret key used for NextAuth.js session encryption
  - Generate using: `openssl rand -base64 32`
  - Keep this secret and never commit it to version control
- `NEXTAUTH_URL`: The base URL of your application
  - Development: `http://localhost:3000`
  - Production: Your production domain

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

## Database Configuration

### PostgreSQL
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `POSTGRES_HOST`: Database host address
- `POSTGRES_PORT`: Database port (default: 5432)
- `DATABASE_URL`: Full PostgreSQL connection string
  - Format: `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}`

To set up PostgreSQL:
1. Install PostgreSQL locally or use a cloud provider (e.g., AWS RDS), supabase, neon.
2. Create a new database and user
3. Note down the credentials and connection details

## Neo4j Configuration

- `NEO4J_HOST`: Neo4j database host URL
- `NEO4J_USERNAME`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `NEO4J_URL`: Full Neo4j connection string

To set up Neo4j:
1. Sign up for [Neo4j Aura](https://neo4j.com/cloud/platform/aura-graph-database/) or install locally
2. Create a new database instance
3. Note down the connection details and credentials

## API Configuration

- `API_V1_PREFIX`: API version prefix (default: `/api`)
- `SECRET_KEY`: Application secret key for encryption
  - Generate using: `openssl rand -base64 32`
- `ALLOWED_HOSTS`: List of allowed CORS origins
  - Development: `["*"]`
  - Production: `["https://your-domain.com"]`

## Email Configuration

### SMTP Settings
- `SMTP_USERNAME`: Email account username
- `SMTP_PASSWORD`: Email account password/app password
- `SMTP_FROM`: Sender email address
- `SMTP_SERVER`: SMTP server address
- `SMTP_PORT`: SMTP port (default: 587)

To set up Gmail SMTP:
1. Use a Gmail account
2. Enable 2-factor authentication
3. Generate an App Password:
   - Go to Google Account > Security
   - Under "2-Step Verification", click "App passwords"
   - Generate a new app password for "Mail"
4. Use the generated password as `SMTP_PASSWORD`

## Nylas Configuration

- `NYLAS_CLIENT_ID`: Nylas API client ID
- `NYLAS_API_KEY`: Nylas API key
- `NYLAS_API_URI`: Nylas API endpoint
- `NYLAS_CALLBACK_URI`: OAuth callback URL
- `NYLAS_WEBHOOK_SECRE`: Webhook secret for Nylas

To obtain Nylas credentials:
1. Sign up for [Nylas](https://www.nylas.com/)
2. Create a new application
3. Configure OAuth settings with your callback URL
4. Note down the client ID and API key

## LLM Configuration

- `LLM_BASE_URL`: Base URL for LLM API
- `LLM_API_KEY`: API key for LLM service

To obtain OpenAI credentials:
1. Sign up for [OpenAI](https://platform.openai.com/)
2. Generate an API key in your account settings
3. Use the API key as `LLM_API_KEY`


## Environment Setup Steps

1. Copy `.env.example` to `.env`
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