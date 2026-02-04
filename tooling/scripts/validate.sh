#!/bin/bash
# validate.sh - Comprehensive validation script for proyectos-aws
# Runs: terraform fmt/validate, yamllint, markdownlint
# Exit codes: 0=success, 1=validation failed

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

echo "=========================================="
echo "🔍 Iniciando validación de tooling"
echo "=========================================="
echo ""

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✓${NC} $message"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠${NC} $message"
        ((WARNINGS++))
    else
        echo -e "${RED}✗${NC} $message"
        ((ERRORS++))
    fi
}

# 1. Terraform validation
echo "📋 Validando archivos Terraform..."
TF_FILES=$(find /workspace -name "*.tf" 2>/dev/null | wc -l)

if [ "$TF_FILES" -gt 0 ]; then
    echo "   Encontrados $TF_FILES archivos .tf"
    
    # Terraform fmt check
    if terraform fmt -check -recursive /workspace > /dev/null 2>&1; then
        print_status "OK" "Terraform format check"
    else
        print_status "FAIL" "Terraform format check - ejecuta 'terraform fmt -recursive'"
    fi
    
    # Terraform validate (requiere init en cada directorio)
    for dir in $(find /workspace -name "*.tf" -exec dirname {} \; | sort -u); do
        echo "   Validando directorio: $dir"
        cd "$dir"
        if [ -f ".terraform.lock.hcl" ] || terraform init -backend=false > /dev/null 2>&1; then
            if terraform validate > /dev/null 2>&1; then
                print_status "OK" "Terraform validate: $dir"
            else
                print_status "FAIL" "Terraform validate: $dir"
            fi
        else
            print_status "WARN" "Terraform validate: $dir (no inicializado, saltando)"
        fi
    done
else
    print_status "WARN" "No se encontraron archivos Terraform (.tf)"
fi

echo ""

# 2. YAML validation
echo "📋 Validando archivos YAML..."
YAML_FILES=$(find /workspace -name "*.yml" -o -name "*.yaml" 2>/dev/null | grep -v ".github" | wc -l)

if [ "$YAML_FILES" -gt 0 ]; then
    echo "   Encontrados $YAML_FILES archivos YAML"
    
    # Create yamllint config if not exists
    if [ ! -f /workspace/.yamllint ]; then
        cat > /tmp/.yamllint <<EOF
extends: default
rules:
  line-length:
    max: 120
    level: warning
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
EOF
        YAMLLINT_CONFIG="/tmp/.yamllint"
    else
        YAMLLINT_CONFIG="/workspace/.yamllint"
    fi
    
    if yamllint -c "$YAMLLINT_CONFIG" /workspace > /dev/null 2>&1; then
        print_status "OK" "YAML lint check"
    else
        print_status "FAIL" "YAML lint check - revisa sintaxis YAML"
        yamllint -c "$YAMLLINT_CONFIG" /workspace || true
    fi
else
    print_status "WARN" "No se encontraron archivos YAML"
fi

echo ""

# 3. Markdown validation
echo "📋 Validando archivos Markdown..."
MD_FILES=$(find /workspace -name "*.md" 2>/dev/null | wc -l)

if [ "$MD_FILES" -gt 0 ]; then
    echo "   Encontrados $MD_FILES archivos Markdown"
    
    # Create markdownlint config if not exists
    if [ ! -f /workspace/.markdownlint.json ]; then
        cat > /tmp/.markdownlint.json <<EOF
{
  "default": true,
  "MD013": { "line_length": 120 },
  "MD033": false,
  "MD041": false
}
EOF
        MDLINT_CONFIG="/tmp/.markdownlint.json"
    else
        MDLINT_CONFIG="/workspace/.markdownlint.json"
    fi
    
    if markdownlint -c "$MDLINT_CONFIG" /workspace/**/*.md > /dev/null 2>&1; then
        print_status "OK" "Markdown lint check"
    else
        print_status "WARN" "Markdown lint check - revisa formato Markdown"
    fi
else
    print_status "WARN" "No se encontraron archivos Markdown"
fi

echo ""

# 4. Security checks (Checkov for IaC)
echo "📋 Ejecutando análisis de seguridad (Checkov)..."
if [ "$TF_FILES" -gt 0 ]; then
    if checkov -d /workspace --quiet --compact > /dev/null 2>&1; then
        print_status "OK" "Checkov security scan"
    else
        print_status "WARN" "Checkov encontró problemas de seguridad (revisar reporte)"
        checkov -d /workspace --compact || true
    fi
else
    print_status "WARN" "No hay archivos IaC para escanear con Checkov"
fi

echo ""
echo "=========================================="
echo "📊 Resumen de validación"
echo "=========================================="
echo -e "Errores:      ${RED}$ERRORS${NC}"
echo -e "Advertencias: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ Validación FALLIDA${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Validación EXITOSA${NC}"
    exit 0
fi
