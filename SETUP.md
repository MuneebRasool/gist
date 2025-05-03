# Gist Project Setup Guide

## Run with Docker

1. **Clone repo:**

   ```bash
   git clone <repository-url>
   cd gist
   ```

2. **Setup env files:**

   * Copy `web/.env.example` → `web/.env.local`
   * Copy `server/.env.example` → `server/.env.local`
   * Setup all the environment variables to make the app work:
      For detailed instructions, see the [environment variables documentation](documentation/environment-variables.md).

3. **Start services:**

   ```bash
   chmod +x start-local.sh
   ./start-local.sh
   ```

## Run without Docker

1. **Web app:**

   ```bash
   cd web
   pnpm i
   pnpm dev
   ```

2. **API:**

   ```bash
   cd server
   uv venv
   uv sync
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
