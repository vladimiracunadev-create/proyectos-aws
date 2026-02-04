#!/bin/bash
# security-verify.sh - Script de verificación completa de seguridad
# Ejecuta todas las verificaciones del security checklist

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "🔍 Verificación de Seguridad - proyectos-aws"
echo -e "==========================================${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅${NC} $message"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️${NC}  $message"
        ((WARNINGS++))
    else
        echo -e "${RED}❌${NC} $message"
        ((ERRORS++))
    fi
}

# 1. Verificar .gitignore
echo -e "${BLUE}1️⃣ Verificando .gitignore...${NC}"
if grep -q "\.tfstate" .gitignore && grep -q "\.env" .gitignore && grep -q "\.pem" .gitignore; then
    print_status "OK" ".gitignore contiene patrones de seguridad"
else
    print_status "FAIL" ".gitignore incompleto"
fi
echo ""

# 2. Verificar pre-commit
echo -e "${BLUE}2️⃣ Verificando pre-commit hooks...${NC}"
if [ -f ".pre-commit-config.yaml" ]; then
    print_status "OK" ".pre-commit-config.yaml existe"
    
    if command -v pre-commit > /dev/null; then
        print_status "OK" "pre-commit instalado"
        echo "   Ejecutando pre-commit checks..."
        if pre-commit run --all-files > /dev/null 2>&1; then
            print_status "OK" "Pre-commit checks pasaron"
        else
            print_status "WARN" "Pre-commit encontró issues (ejecuta: pre-commit run --all-files)"
        fi
    else
        print_status "WARN" "pre-commit no instalado (instala con: pip install pre-commit)"
    fi
else
    print_status "FAIL" ".pre-commit-config.yaml no encontrado"
fi
echo ""

# 3. Verificar GitHub Actions
echo -e "${BLUE}3️⃣ Verificando GitHub Actions...${NC}"
if [ -f ".github/workflows/security-scan.yml" ]; then
    print_status "OK" "security-scan.yml configurado"
else
    print_status "FAIL" "security-scan.yml no encontrado"
fi
echo ""

# 4. Verificar Docker security
echo -e "${BLUE}4️⃣ Verificando seguridad de Docker...${NC}"
if [ -f "tooling/Dockerfile.tooling" ]; then
    print_status "OK" "Dockerfile.tooling existe"
    
    if grep -q "USER tooling" tooling/Dockerfile.tooling; then
        print_status "OK" "Dockerfile usa usuario no-root"
    else
        print_status "FAIL" "Dockerfile no especifica usuario no-root"
    fi
    
    if grep -q "HEALTHCHECK" tooling/Dockerfile.tooling; then
        print_status "OK" "Dockerfile incluye HEALTHCHECK"
    else
        print_status "WARN" "Dockerfile no incluye HEALTHCHECK"
    fi
    
    if docker images | grep -q "proyectos-aws/tooling"; then
        USER=$(docker run --rm proyectos-aws/tooling:1.0.0 whoami 2>/dev/null || echo "error")
        if [ "$USER" = "tooling" ]; then
            print_status "OK" "Contenedor corre como usuario no-root: $USER"
        elif [ "$USER" = "error" ]; then
            print_status "WARN" "No se pudo verificar usuario del contenedor"
        else
            print_status "FAIL" "Contenedor corre como: $USER (debería ser 'tooling')"
        fi
    else
        print_status "WARN" "Imagen de tooling no construida (ejecuta: make tooling-build)"
    fi
else
    print_status "FAIL" "Dockerfile.tooling no encontrado"
fi
echo ""

# 5. Verificar Kubernetes security
echo -e "${BLUE}5️⃣ Verificando seguridad de Kubernetes...${NC}"
if [ -f "k8s/tooling-job/job.yaml" ]; then
    print_status "OK" "job.yaml existe"
    
    if grep -q "runAsNonRoot: true" k8s/tooling-job/job.yaml; then
        print_status "OK" "Job configura runAsNonRoot"
    else
        print_status "FAIL" "Job no configura runAsNonRoot"
    fi
    
    if grep -q "readOnlyRootFilesystem: true" k8s/tooling-job/job.yaml; then
        print_status "OK" "Job configura readOnlyRootFilesystem"
    else
        print_status "WARN" "Job no configura readOnlyRootFilesystem"
    fi
    
    if grep -q "resources:" k8s/tooling-job/job.yaml; then
        print_status "OK" "Job define resource limits"
    else
        print_status "FAIL" "Job no define resource limits"
    fi
else
    print_status "FAIL" "k8s/tooling-job/job.yaml no encontrado"
fi

if [ -f "k8s/tooling-job/networkpolicy.yaml" ]; then
    print_status "OK" "NetworkPolicy configurada"
else
    print_status "WARN" "NetworkPolicy no encontrada"
fi
echo ""

# 6. Verificar documentación
echo -e "${BLUE}6️⃣ Verificando documentación de seguridad...${NC}"
DOCS=("SECURITY.md" "docs/killed.md" "docs/TOOLING.md" "docs/SECURITY_CHECKLIST.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        print_status "OK" "$doc existe"
    else
        print_status "FAIL" "$doc no encontrado"
    fi
done
echo ""

# 7. Buscar secretos potenciales
echo -e "${BLUE}7️⃣ Buscando secretos potenciales...${NC}"
if command -v detect-secrets > /dev/null; then
    if [ -f ".secrets.baseline" ]; then
        print_status "OK" ".secrets.baseline existe"
        if detect-secrets scan --baseline .secrets.baseline > /dev/null 2>&1; then
            print_status "OK" "No se detectaron secretos nuevos"
        else
            print_status "WARN" "Se detectaron posibles secretos (revisa con: detect-secrets scan)"
        fi
    else
        print_status "WARN" ".secrets.baseline no encontrado"
    fi
else
    print_status "WARN" "detect-secrets no instalado (instala con: pip install detect-secrets)"
fi
echo ""

# 8. Verificar Makefile
echo -e "${BLUE}8️⃣ Verificando Makefile...${NC}"
if [ -f "Makefile" ]; then
    print_status "OK" "Makefile existe"
    
    REQUIRED_TARGETS=("tooling-build" "tooling-validate" "security-scan" "k8s-demo")
    for target in "${REQUIRED_TARGETS[@]}"; do
        if grep -q "^$target:" Makefile; then
            print_status "OK" "Target '$target' definido"
        else
            print_status "FAIL" "Target '$target' no encontrado"
        fi
    done
else
    print_status "FAIL" "Makefile no encontrado"
fi
echo ""

# 9. Verificar Hub CLI
echo -e "${BLUE}9️⃣ Verificando Hub CLI...${NC}"
if [ -f "hub.sh" ]; then
    print_status "OK" "hub.sh existe"
    if [ -x "hub.sh" ]; then
        print_status "OK" "hub.sh es ejecutable"
    else
        print_status "WARN" "hub.sh no es ejecutable (ejecuta: chmod +x hub.sh)"
    fi
else
    print_status "FAIL" "hub.sh no encontrado"
fi

if [ -f "hub.ps1" ]; then
    print_status "OK" "hub.ps1 existe"
else
    print_status "FAIL" "hub.ps1 no encontrado"
fi
echo ""

# Resumen final
echo -e "${BLUE}=========================================="
echo "📊 Resumen de Verificación"
echo -e "==========================================${NC}"
echo -e "Errores:      ${RED}$ERRORS${NC}"
echo -e "Advertencias: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ Verificación FALLIDA - Hay errores críticos que deben corregirse${NC}"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Verificación COMPLETADA con advertencias${NC}"
    echo -e "${YELLOW}   Revisa las advertencias para mejorar la seguridad${NC}"
    exit 0
else
    echo -e "${GREEN}✅ Verificación EXITOSA - Todas las medidas de seguridad están implementadas${NC}"
    exit 0
fi
