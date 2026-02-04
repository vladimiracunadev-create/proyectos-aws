#!/bin/bash
# hub.sh - Hub CLI para proyectos-aws (Linux/Mac)
# Comandos: list-projects, validate

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
show_help() {
    cat <<EOF
${GREEN}🚀 Hub CLI - proyectos-aws${NC}

${BLUE}Uso:${NC}
  ./hub.sh <comando>

${BLUE}Comandos disponibles:${NC}
  ${GREEN}list-projects${NC}    Lista todos los proyectos AWS (carpetas aws-*)
  ${GREEN}validate${NC}          Ejecuta validaciones usando tooling Docker
  ${GREEN}help${NC}              Muestra esta ayuda

${BLUE}Ejemplos:${NC}
  ./hub.sh list-projects
  ./hub.sh validate

${BLUE}Requisitos:${NC}
  - Docker instalado y corriendo
  - make (para comandos avanzados)

EOF
}

list_projects() {
    echo -e "${GREEN}📂 Proyectos AWS encontrados:${NC}"
    echo ""
    
    local count=0
    for dir in "$SCRIPT_DIR"/aws-*; do
        if [ -d "$dir" ]; then
            local project_name=$(basename "$dir")
            local file_count=$(find "$dir" -type f | wc -l)
            echo -e "  ${BLUE}▸${NC} $project_name ${YELLOW}($file_count archivos)${NC}"
            ((count++))
        fi
    done
    
    echo ""
    if [ $count -eq 0 ]; then
        echo -e "${YELLOW}⚠️  No se encontraron proyectos (carpetas aws-*)${NC}"
    else
        echo -e "${GREEN}✅ Total: $count proyecto(s)${NC}"
    fi
}

validate() {
    echo -e "${GREEN}🔍 Ejecutando validaciones con tooling...${NC}"
    echo ""
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Error: Docker no está corriendo${NC}"
        echo -e "${YELLOW}   Inicia Docker y vuelve a intentar${NC}"
        exit 1
    fi
    
    # Check if tooling image exists
    if ! docker images | grep -q "proyectos-aws/tooling"; then
        echo -e "${YELLOW}⚠️  Imagen de tooling no encontrada. Construyendo...${NC}"
        make tooling-build
        echo ""
    fi
    
    # Run validation
    make tooling-validate
}

# Main
case "${1:-help}" in
    list-projects)
        list_projects
        ;;
    validate)
        validate
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando desconocido: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
