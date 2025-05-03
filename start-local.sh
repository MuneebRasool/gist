#!/bin/bash

set -e  # Exit on error
trap 'echo "Error at line $LINENO: $BASH_COMMAND"' ERR

echo "🚀 Starting Gist local development environment..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install it first."
    exit 1
fi

# Check for Docker Compose
if command -v docker-compose &> /dev/null; then
    docker_compose="docker-compose"
elif docker compose version &> /dev/null; then
    docker_compose="docker compose"
else
    echo "❌ Docker Compose is not available. Please install it."
    exit 1
fi

for port in 3000 5432 7474 7687 8000; do
    echo "🔍 Checking port $port..."

    # Stop any docker container binding this port
    container_id=$(docker ps -q --filter "publish=$port")
    if [ -n "$container_id" ]; then
        echo "   🛑 Stopping container using port $port (Container ID: $container_id)"
        docker stop $container_id || echo "   ❌ Failed to stop container $container_id"
    fi

    # Kill any local process binding this port
    pid=$(lsof -ti tcp:$port) || true
    if [ -n "$pid" ]; then
        echo "   🔥 Killing process on port $port (PID: $pid)"
        kill -9 $pid || echo "   ❌ Failed to kill PID $pid"
    fi
done

# Clean up old containers
echo "🧹 Cleaning up old containers..."
$docker_compose -f docker-compose-local.yml down --remove-orphans || true
docker rm -f gist-postgres gist-neo4j gist-api gist-web 2>/dev/null || true

# Copy env files if missing
[ -f web/.env.local ] || cp web/.env.local web/.env.local 2>/dev/null || echo "⚠️ Missing web/.env.local"
[ -f server/.env.local ] || cp server/.env.local server/.env.local 2>/dev/null || echo "⚠️ Missing server/.env.local"

# Start containers
echo "🔨 Building and starting containers..."
$docker_compose -f docker-compose-local.yml up -d

echo "⏳ Waiting for services to be ready..."
sleep 15

# Run migrations
echo "🔄 Running migrations..."
$docker_compose -f docker-compose-local.yml exec -T api aerich migrate || echo "⚠️ Migrate failed"
$docker_compose -f docker-compose-local.yml exec -T api aerich upgrade || echo "⚠️ Upgrade failed"

# Success message
echo "✅ Gist environment is running!"
echo "🌐 Web:     http://localhost:3000"
echo "📦 API:     http://localhost:8000/"
echo "🧠 Neo4j:   http://localhost:7474"
echo ""
eccho "💡 In case migration fails, you can run the "aerich migrate" command manually in the postgres container or try resetting the postgres container"
echo "💡 To stop: $docker_compose -f docker-compose-local.yml down"
echo "💡 To logs: $docker_compose -f docker-compose-local.yml logs -f"
echo "💡 Clean run: $docker_compose -f docker-compose-local.yml down -v && ./start-local.sh"
echo "💡 To run in detached mode: $docker_compose -f docker-compose-local.yml up -d"
