# Environment Variables

This document lists the key environment variables for GIST.

## Frontend Variables

```env
NEXTAUTH_SECRET=
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

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
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:$
```
