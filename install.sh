#!/bin/bash

# RPGer Content Extractor - Quick Install Script
# Usage: curl -sSL https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="rpger-extractor"
GITHUB_RAW_URL="https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main"
DOCKER_IMAGE="padster2012/rpger-content-extractor:latest"

# Helper functions
print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                🎮 RPGer Content Extractor                    ║"
    echo "║                    Quick Install Script                      ║"
    echo "║                        v1.0.44                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependencies() {
    print_step "Checking dependencies..."

    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check for Docker Compose (both standalone and plugin versions)
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
        print_success "Found docker-compose (standalone version)"
    elif docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
        print_success "Found docker compose (plugin version)"
    else
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        echo "Or install Docker Desktop which includes Docker Compose"
        exit 1
    fi

    print_success "Dependencies check passed"
}

create_install_directory() {
    print_step "Creating installation directory..."
    
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Directory '$INSTALL_DIR' already exists"
        read -p "Do you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Installation cancelled"
            exit 1
        fi
    else
        mkdir -p "$INSTALL_DIR"
        print_success "Created directory '$INSTALL_DIR'"
    fi
    
    cd "$INSTALL_DIR"
}

download_files() {
    print_step "Downloading configuration files..."
    
    # Download docker-compose files
    curl -sSL "$GITHUB_RAW_URL/docker-compose.yml" -o docker-compose.yml
    curl -sSL "$GITHUB_RAW_URL/docker-compose.dev.yml" -o docker-compose.dev.yml
    
    # Try to download docker-compose.containers.yml (might not exist)
    if curl -sSL "$GITHUB_RAW_URL/docker-compose.containers.yml" -o docker-compose.containers.yml 2>/dev/null; then
        print_success "Downloaded docker-compose.containers.yml"
    else
        print_warning "docker-compose.containers.yml not found, creating basic version..."
        create_containers_compose
    fi
    
    print_success "Downloaded configuration files"
}

create_containers_compose() {
    cat > docker-compose.containers.yml << 'EOF'
version: '3.8'

services:
  mongodb:
    image: mongo:7-jammy
    container_name: rpger-mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_DATABASE: rpger
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    networks:
      - rpger-network

  chromadb:
    image: chromadb/chroma:latest
    container_name: rpger-chromadb
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - chromadb_data:/chroma/chroma
    networks:
      - rpger-network

networks:
  rpger-network:
    driver: bridge

volumes:
  mongodb_data:
  chromadb_data:
EOF
}

show_deployment_menu() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Deployment Options                       ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  1. 🚀 Production (Recommended)                             ║"
    echo "║     • Uses pre-built Docker images (v1.0.44)               ║"
    echo "║     • Requires external MongoDB & ChromaDB                  ║"
    echo "║     • Fastest startup, minimal resources                    ║"
    echo "║                                                              ║"
    echo "║  2. 🛠️  Development                                         ║"
    echo "║     • Builds from source with live reloading               ║"
    echo "║     • Requires external MongoDB & ChromaDB                  ║"
    echo "║     • For code development and testing                      ║"
    echo "║                                                              ║"
    echo "║  3. 🗄️  Full Stack                                          ║"
    echo "║     • Includes MongoDB & ChromaDB containers               ║"
    echo "║     • Self-contained, no external dependencies             ║"
    echo "║     • Higher resource usage (~2GB RAM)                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    while true; do
        read -p "Select deployment option (1-3): " choice
        case $choice in
            1) DEPLOYMENT_MODE="production"; break;;
            2) DEPLOYMENT_MODE="development"; break;;
            3) DEPLOYMENT_MODE="fullstack"; break;;
            *) print_error "Invalid choice. Please select 1, 2, or 3.";;
        esac
    done
}

configure_environment() {
    print_step "Configuring environment..."

    # Check if .env already exists
    if [ -f ".env" ]; then
        print_warning ".env file already exists"
        read -p "Do you want to reconfigure it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_success "Keeping existing .env file"
            return
        fi
        cp .env .env.backup
        print_success "Backed up existing .env to .env.backup"
    fi

    # Create new .env file
    cat > .env << 'ENVEOF'
# RPGer Content Extractor Configuration
# Generated by install script

# Flask Configuration
FLASK_ENV=production
MAX_CONTENT_LENGTH=200
UPLOAD_TIMEOUT=300

# Database Configuration (will be set based on deployment mode)
MONGODB_URL=
CHROMADB_URL=

# AI Provider API Keys (Optional)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
OPENROUTER_API_KEY=

# Advanced Configuration
LOG_LEVEL=INFO
WORKERS=1
ENVEOF

    # Set database URLs based on deployment mode
    case $DEPLOYMENT_MODE in
        "fullstack")
            sed -i 's|MONGODB_URL=|MONGODB_URL=mongodb://mongodb:27017|' .env
            sed -i 's|CHROMADB_URL=|CHROMADB_URL=http://chromadb:8000|' .env
            ;;
        "production"|"development")
            configure_external_databases
            ;;
    esac

    configure_api_keys
    print_success "Environment configured"
}

configure_external_databases() {
    echo -e "${YELLOW}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                External Database Configuration               ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    # MongoDB Configuration
    echo -e "${CYAN}MongoDB Configuration:${NC}"
    read -p "MongoDB URL (e.g., mongodb://localhost:27017): " mongodb_url
    if [ -n "$mongodb_url" ]; then
        sed -i "s|MONGODB_URL=|MONGODB_URL=$mongodb_url|" .env
    else
        print_warning "MongoDB URL not set - you'll need to configure this later"
    fi

    # ChromaDB Configuration
    echo -e "${CYAN}ChromaDB Configuration:${NC}"
    read -p "ChromaDB URL (e.g., http://localhost:8000): " chromadb_url
    if [ -n "$chromadb_url" ]; then
        sed -i "s|CHROMADB_URL=|CHROMADB_URL=$chromadb_url|" .env
    else
        print_warning "ChromaDB URL not set - you'll need to configure this later"
    fi
}

configure_api_keys() {
    echo -e "${YELLOW}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   AI Provider API Keys                      ║"
    echo "║                      (Optional)                             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    read -p "Do you want to configure AI API keys now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}Anthropic Claude API Key:${NC}"
        read -s -p "Enter key (or press Enter to skip): " anthropic_key
        echo
        if [ -n "$anthropic_key" ]; then
            sed -i "s|ANTHROPIC_API_KEY=|ANTHROPIC_API_KEY=$anthropic_key|" .env
        fi

        echo -e "${CYAN}OpenAI API Key:${NC}"
        read -s -p "Enter key (or press Enter to skip): " openai_key
        echo
        if [ -n "$openai_key" ]; then
            sed -i "s|OPENAI_API_KEY=|OPENAI_API_KEY=$openai_key|" .env
        fi

        echo -e "${CYAN}OpenRouter API Key:${NC}"
        read -s -p "Enter key (or press Enter to skip): " openrouter_key
        echo
        if [ -n "$openrouter_key" ]; then
            sed -i "s|OPENROUTER_API_KEY=|OPENROUTER_API_KEY=$openrouter_key|" .env
        fi
    else
        print_warning "API keys not configured - you can add them to .env later"
    fi
}

create_startup_scripts() {
    print_step "Creating startup scripts..."

    # Production startup script
    cat > start-production.sh << STARTEOF
#!/bin/bash
echo "🚀 Starting RPGer Content Extractor (Production Mode)"
$DOCKER_COMPOSE_CMD pull
$DOCKER_COMPOSE_CMD up -d
echo "✅ Started! Access at: http://localhost:5000"
echo "📊 Check status: $DOCKER_COMPOSE_CMD ps"
echo "📋 View logs: $DOCKER_COMPOSE_CMD logs -f app"
STARTEOF
    chmod +x start-production.sh

    # Development startup script
    cat > start-development.sh << STARTEOF
#!/bin/bash
echo "🛠️ Starting RPGer Content Extractor (Development Mode)"
$DOCKER_COMPOSE_CMD -f docker-compose.dev.yml up -d --build
echo "✅ Started! Access at: http://localhost:5000"
echo "📊 Check status: $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml ps"
echo "📋 View logs: $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml logs -f app"
STARTEOF
    chmod +x start-development.sh

    # Full stack startup script
    cat > start-fullstack.sh << STARTEOF
#!/bin/bash
echo "🗄️ Starting RPGer Content Extractor (Full Stack Mode)"
$DOCKER_COMPOSE_CMD -f docker-compose.yml -f docker-compose.containers.yml up -d
echo "✅ Started! Access at: http://localhost:5000"
echo "📊 Check status: $DOCKER_COMPOSE_CMD ps"
echo "📋 View logs: $DOCKER_COMPOSE_CMD logs -f app"
echo "🗃️ MongoDB: localhost:27017"
echo "🔍 ChromaDB: localhost:8000"
STARTEOF
    chmod +x start-fullstack.sh

    # Stop script
    cat > stop.sh << STARTEOF
#!/bin/bash
echo "🛑 Stopping RPGer Content Extractor..."
$DOCKER_COMPOSE_CMD down 2>/dev/null || true
$DOCKER_COMPOSE_CMD -f docker-compose.dev.yml down 2>/dev/null || true
$DOCKER_COMPOSE_CMD -f docker-compose.yml -f docker-compose.containers.yml down 2>/dev/null || true
echo "✅ Stopped!"
STARTEOF
    chmod +x stop.sh

    print_success "Created startup scripts"
}

show_completion_message() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                🎉 Installation Complete! 🎉                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo -e "${CYAN}📁 Installation Directory:${NC} $(pwd)"
    echo -e "${CYAN}🐳 Docker Image:${NC} $DOCKER_IMAGE"
    echo -e "${CYAN}⚙️  Deployment Mode:${NC} $DEPLOYMENT_MODE"
    echo

    case $DEPLOYMENT_MODE in
        "production")
            echo -e "${YELLOW}🚀 To start (Production):${NC}"
            echo "   ./start-production.sh"
            ;;
        "development")
            echo -e "${YELLOW}🛠️ To start (Development):${NC}"
            echo "   ./start-development.sh"
            ;;
        "fullstack")
            echo -e "${YELLOW}🗄️ To start (Full Stack):${NC}"
            echo "   ./start-fullstack.sh"
            ;;
    esac

    echo
    echo -e "${YELLOW}📋 Other commands:${NC}"
    echo "   ./stop.sh                    # Stop all services"
    echo "   $DOCKER_COMPOSE_CMD ps            # Check status"
    echo "   $DOCKER_COMPOSE_CMD logs -f app   # View logs"
    echo
    echo -e "${YELLOW}🌐 Access:${NC}"
    echo "   Web UI: http://localhost:5000"
    echo "   Health: http://localhost:5000/health"

    if [ "$DEPLOYMENT_MODE" = "fullstack" ]; then
        echo "   MongoDB: localhost:27017"
        echo "   ChromaDB: localhost:8000"
    fi

    echo
    echo -e "${YELLOW}📝 Configuration:${NC}"
    echo "   Edit .env file to modify settings"
    echo "   Backup created: .env.backup (if existed)"
    echo
    echo -e "${GREEN}🎮 Happy RPG content extracting! 🎮${NC}"
}

# Main execution
main() {
    print_header
    check_dependencies
    create_install_directory
    download_files
    show_deployment_menu
    configure_environment
    create_startup_scripts
    show_completion_message
}

# Run main function
main "$@"
