#!/bin/bash
# Remove set -e to prevent early exits on non-critical errors
# Add error trapping for debugging
trap 'echo "Error at line $LINENO, command: $BASH_COMMAND"' ERR

echo "🚀 Starting GIST local development environment..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if lsof is installed
if ! command -v lsof &> /dev/null; then
    echo "⚠️ lsof command not found. Attempting to install..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y lsof
    elif command -v yum &> /dev/null; then
        sudo yum install -y lsof
    elif command -v brew &> /dev/null; then
        brew install lsof
    else
        echo "❌ Could not install lsof automatically. Please install it manually."
        echo "⚠️ Continuing without port conflict resolution."
    fi
fi

# Function to check and free port with multiple methods
check_and_free_port() {
    local port=$1
    local use_sudo=$2
    
    echo "🔎 Checking port $port..."
    
    # List processes using the port with lsof
    if [ "$use_sudo" = "true" ]; then
        echo "   Using sudo lsof to check port $port:"
        sudo lsof -i:$port -P -n || echo "   No process found with sudo lsof"
        
        # Try to kill any process using this port
        pid=$(sudo lsof -ti:$port 2>/dev/null)
        if [ ! -z "$pid" ]; then
            echo "   🔥 Found process $pid using port $port. Killing with sudo..."
            sudo kill -9 $pid
        fi
        
        # Special handling for docker-proxy processes
        if sudo lsof -i:$port -P -n | grep -q 'docker-pr'; then
            echo "   🔥 Found docker-proxy processes using port $port. Restarting Docker service..."
            sudo systemctl restart docker || {
                echo "   ⚠️ Could not restart Docker service. Will try to kill docker-proxy processes directly..."
                sudo pkill -f "docker-proxy.*:$port" || echo "   ❌ Failed to kill docker-proxy processes"
            }
            sleep 3  # Give Docker time to clean up
        fi
        
        # Try fuser as an alternative
        echo "   Using sudo fuser to check port $port:"
        sudo fuser $port/tcp 2>/dev/null || echo "   No process found with sudo fuser"
        sudo fuser -k $port/tcp 2>/dev/null || echo "   Failed to kill with sudo fuser"
    else
        echo "   Using lsof to check port $port:"
        lsof -i:$port -P -n || echo "   No process found with lsof"
        
        # Try to kill any process using this port
        pid=$(lsof -ti:$port 2>/dev/null || true)
        if [ ! -z "$pid" ]; then
            echo "   ⚠️ Found process $pid using port $port. Attempting to kill..."
            kill -9 $pid 2>/dev/null || echo "   Failed to kill process $pid"
        fi
    fi
    
    # Look for Docker containers using this port
    echo "   Checking Docker containers using port $port:"
    docker ps -a --format "{{.ID}}: {{.Names}} - {{.Ports}}" | grep ":$port" || echo "   No Docker container found using port $port"
}

echo "🛑 Stopping Docker containers first..."
docker-compose -f docker-compose-local.yml down --remove-orphans 2>/dev/null || echo "⚠️ No running containers found."
docker rm -f gist-postgres gist-neo4j gist-api gist-web 2>/dev/null || echo "⚠️ Some containers could not be removed."

echo "🔍 Checking for processes using required ports..."
# First try without sudo
for port in 3000 5432 7474 7687 8000; do
    check_and_free_port $port false
done

# Special handling for port 7474 - it's causing most issues
echo "🔬 Special handling for port 7474..."
if lsof -i:7474 -P -n | grep -q "LISTEN" || netstat -tuln 2>/dev/null | grep -q ":7474 " || ss -tuln | grep -q ":7474 "; then
    echo "⚠️ Port 7474 is still in use after initial clearing attempt."
    echo "   Attempting with sudo privileges..."
    check_and_free_port 7474 true
    
    echo "   Checking for neo4j service..."
    if systemctl is-active --quiet neo4j 2>/dev/null; then
        echo "   🛑 Found running neo4j service, stopping it..."
        sudo systemctl stop neo4j
    fi
    
    # Final check
    if lsof -i:7474 -P -n | grep -q "LISTEN" || netstat -tuln 2>/dev/null | grep -q ":7474 " || ss -tuln | grep -q ":7474 "; then
        echo "⚠️ WARNING: Port 7474 is STILL in use after multiple clearing attempts!"
        echo "   Last resort - restarting Docker service completely..."
        echo "   This will stop all running Docker containers!"
        read -p "   Do you want to restart Docker service? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo systemctl restart docker
            sleep 5  # Wait for Docker to restart
        else
            echo "⚠️ Continuing without restarting Docker. This may fail."
        fi
    fi
fi

echo "🧹 Cleaning up any existing containers..."
docker-compose -f docker-compose-local.yml down --remove-orphans 2>/dev/null || echo "⚠️ No containers to clean up."
docker rm -f gist-postgres gist-neo4j gist-api gist-web 2>/dev/null || echo "⚠️ Some containers could not be removed."

# Check if docker-compose command exists
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Checking for docker compose plugin..."
    if docker compose version &> /dev/null; then
        echo "✅ Using docker compose plugin instead of docker-compose"
        # Create alias for the rest of the script
        docker_compose="docker compose"
    else
        echo "❌ Neither docker-compose nor docker compose plugin are available. Please install one of them."
        exit 1
    fi
else
    docker_compose="docker-compose"
fi

if [ ! -f web/.env.local ]; then
    echo "⚠️ web/.env.local file not found, creating from example..."
    cp web/.env.local.example web/.env.local 2>/dev/null || cp web/.env web/.env.local 2>/dev/null || echo "⚠️ Could not create web/.env.local file. Please create it manually."
fi

if [ ! -f server/.env ]; then
    echo "⚠️ server/.env file not found, creating from example..."
    cp server/.env.example server/.env 2>/dev/null || echo "❌ Could not create server/.env file. Please create it manually."
fi

echo "🔨 Building and starting containers..."
$docker_compose -f docker-compose-local.yml up -d || {
    echo "❌ Failed to start containers. See error above."
    exit 1
}

echo "⏳ Waiting for services to be ready..."
sleep 15

echo "🔄 Running database migrations..."
$docker_compose -f docker-compose-local.yml exec -T api aerich migrate || echo "❌ Migration creation failed, but continuing..."
$docker_compose -f docker-compose-local.yml exec -T api aerich upgrade || echo "❌ Migration upgrade failed, but continuing..."

echo "✅ GIST development environment is now running!"
echo "📊 Web UI: http://localhost:3000"
echo "🔌 API: http://localhost:8000/api"
echo "📊 Neo4j Browser: http://localhost:7474"
echo ""
echo "💡 To stop the environment, run: $docker_compose -f docker-compose-local.yml down"
echo "💡 To view logs, run: $docker_compose -f docker-compose-local.yml logs -f"
echo "💡 To restart with a clean environment, run: $docker_compose -f docker-compose-local.yml down -v && ./start-local.sh" 