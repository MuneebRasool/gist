# GIST Project Setup Guide

This guide covers both local development setup using Docker and cloud deployment options.

## Local Development Setup

### Prerequisites

- Docker (latest version)
- Docker Compose (V2 preferred)
- Available ports: 3000 (Web), 5432 (PostgreSQL), 7474/7687 (Neo4j), 8000 (API)

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd GIST
```

2. Set up environment files:
   - Copy `web/.env.local.example` to `web/.env.local`
   - Copy `server/.env.local.example` to `server/.env.local`

3. Start the development environment:
```bash
chmod +x start-local.sh  # Make script executable
./start-local.sh
```

### What start-local.sh Does

The script automates the following:
- Checks for Docker and Docker Compose installation
- Frees up required ports (3000, 5432, 7474, 7687, 8000)
- Cleans up old containers
- Sets up environment files
- Starts all services using docker-compose
- Runs database migrations

### Accessing Services

After successful startup, you can access:
- Web Application: http://localhost:3000
- API: http://localhost:8000
- Neo4j Browser: http://localhost:7474

### Common Commands

```bash
# View logs
docker compose -f docker-compose-local.yml logs -f

# Stop all services
docker compose -f docker-compose-local.yml down

# Clean restart (removes volumes)
docker compose -f docker-compose-local.yml down -v && ./start-local.sh
```

### Common Issues and Solutions

1. **Port Conflicts**
   - Error: "port is already allocated"
   - Solution: Manually kill processes using these ports:
     ```bash
     sudo lsof -i :3000  # Replace with conflicting port
     sudo kill -9 <PID>
     ```

2. **Docker Permission Issues**
   - Error: "permission denied while trying to connect to the Docker daemon socket"
   - Solution: Add your user to docker group:
     ```bash
     sudo usermod -aG docker $USER
     newgrp docker
     ```

3. **Database Migration Failures**
   - Error: "migrate failed" or "upgrade failed"
   - Solution: Try resetting the databases:
     ```bash
     docker compose -f docker-compose-local.yml down -v
     ./start-local.sh
     ```


## setting up yourself : 


```bash
cd web
pnpm i
pnpm dev
```


```bash
cd server
uv venv
uv sync
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Cloud Deployment

### Cloud Services Setup

#### PostgreSQL

1. **Using AWS RDS**:
   - Create a PostgreSQL instance in RDS
   - Configure security groups to allow access
   - Update `server/.env` with:
     ```
     DATABASE_URL=postgresql://user:password@your-rds-endpoint:5432/dbname
     ```

2. **Using Digital Ocean**:
   - Create a managed PostgreSQL database
   - Configure trusted sources
   - Use the provided connection string in your environment

#### Neo4j

1. **Using Neo4j Aura**:
   - Create a free/professional instance on Neo4j Aura
   - Get the connection credentials
   - Update `server/.env` with:
     ```
     NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
     NEO4J_USERNAME=neo4j
     NEO4J_PASSWORD=your-password
     ```

2. **Self-hosted Neo4j**:
   - Deploy Neo4j on your preferred cloud provider
   - Configure HTTPS and authentication
   - Update environment variables accordingly




### Environment Configuration

For cloud deployment, ensure these environment variables are properly set:

```env
# Database Configurations
DATABASE_URL=your-postgres-url
NEO4J_URI=your-neo4j-uri
NEO4J_USERNAME=your-username
NEO4J_PASSWORD=your-password

# API Configuration
API_HOST=your-api-domain
API_PORT=8000

# Web Configuration
NEXT_PUBLIC_API_URL=https://your-api-domain
```

### Security Considerations

1. Always use SSL/TLS for database connections
2. Implement proper firewall rules
3. Use secure password policies
4. Enable database backups
5. Monitor database metrics and set up alerts

### Deployment Checklist

- [ ] Configure environment variables
- [ ] Set up databases and run migrations
- [ ] Configure domain names and SSL certificates
- [ ] Set up monitoring and logging
- [ ] Configure backup solutions
- [ ] Test all connections and functionalities
