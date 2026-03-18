#!/usr/bin/env bash
# =============================================================================
# deploy-evidence-destroy.sh
# Ciclo automatizado: terraform apply → captura manual → terraform destroy
#
# Uso:
#   ./scripts/gameday/deploy-evidence-destroy.sh caso-j [minutos]
#   ./scripts/gameday/deploy-evidence-destroy.sh caso-k [minutos]
#
# Ejemplos:
#   ./scripts/gameday/deploy-evidence-destroy.sh caso-j        # 30 min por defecto
#   ./scripts/gameday/deploy-evidence-destroy.sh caso-k 20     # 20 min de ventana
#
# Requisitos:
#   - terraform instalado y en PATH
#   - AWS CLI configurado (o variables AWS_ACCESS_KEY_ID etc.)
#   - jq instalado (para leer outputs de terraform)
# =============================================================================

set -euo pipefail

# ─── Colores ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ─── Argumentos ───────────────────────────────────────────────────────────────
CASO="${1:-}"
TIMER_MINUTES="${2:-30}"

if [[ -z "$CASO" ]]; then
  echo -e "${RED}ERROR: Debes indicar el caso.${NC}"
  echo -e "Uso: $0 caso-j|caso-k [minutos_ventana]"
  exit 1
fi

# ─── Configuracion por caso ───────────────────────────────────────────────────
case "$CASO" in
  caso-j)
    TERRAFORM_DIR="caso-j-containers-ecs/terraform"
    CASO_NOMBRE="Caso J — ECS Fargate + ALB"
    COST_WARNING="⚠️  ECS Fargate + ALB cobra desde la primera hora (~\$0.02/min activo)"
    OUTPUT_URL_KEY="alb_dns_name"
    URL_PREFIX="http://"
    ;;
  caso-k)
    TERRAFORM_DIR="caso-k-kubernetes-eks/terraform"
    CASO_NOMBRE="Caso K — Kubernetes EKS"
    COST_WARNING="🚨 EKS control plane + NAT Gateway cobran ~\$0.002/min — destruir INMEDIATAMENTE al terminar"
    OUTPUT_URL_KEY="cluster_endpoint"
    URL_PREFIX=""
    ;;
  *)
    echo -e "${RED}ERROR: Caso no reconocido: '$CASO'${NC}"
    echo -e "Casos soportados: caso-j, caso-k"
    exit 1
    ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TF_PATH="$REPO_ROOT/$TERRAFORM_DIR"

# ─── Verificaciones previas ───────────────────────────────────────────────────
echo -e "\n${BOLD}${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${BLUE}  GameDay: $CASO_NOMBRE${NC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${NC}\n"

echo -e "${CYAN}Verificando prerequisitos...${NC}"

if ! command -v terraform &>/dev/null; then
  echo -e "${RED}ERROR: terraform no encontrado en PATH${NC}"
  exit 1
fi

if ! command -v aws &>/dev/null; then
  echo -e "${RED}ERROR: aws CLI no encontrado en PATH${NC}"
  exit 1
fi

if [[ ! -d "$TF_PATH" ]]; then
  echo -e "${RED}ERROR: Directorio terraform no encontrado: $TF_PATH${NC}"
  exit 1
fi

# Verificar credenciales AWS
if ! aws sts get-caller-identity &>/dev/null; then
  echo -e "${RED}ERROR: No hay credenciales AWS configuradas${NC}"
  echo -e "Configura AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY, o usa 'aws configure'"
  exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✓ AWS autenticado — cuenta: $ACCOUNT_ID${NC}"
echo -e "${GREEN}✓ Terraform disponible: $(terraform version -json | python3 -c 'import sys,json; print(json.load(sys.stdin)["terraform_version"])' 2>/dev/null || terraform version | head -1)${NC}"

# ─── Advertencia de costo ─────────────────────────────────────────────────────
echo -e "\n${YELLOW}${COST_WARNING}${NC}"
echo -e "${YELLOW}Ventana asignada: ${BOLD}${TIMER_MINUTES} minutos${NC}${YELLOW} — al expirar se ejecuta destroy automaticamente${NC}\n"

read -rp "$(echo -e ${BOLD}"¿Confirmas iniciar el GameDay? (escribe 'si' para continuar): "${NC})" CONFIRM
if [[ "$CONFIRM" != "si" ]]; then
  echo -e "${YELLOW}Cancelado.${NC}"
  exit 0
fi

# ─── FASE 1: Terraform Apply ──────────────────────────────────────────────────
echo -e "\n${BOLD}${GREEN}▶ FASE 1: terraform apply${NC}"
echo -e "${CYAN}Directorio: $TF_PATH${NC}\n"

APPLY_START=$(date +%s)

cd "$TF_PATH"
terraform init -upgrade -no-color 2>&1 | tail -5
echo ""
terraform apply -auto-approve -no-color

APPLY_END=$(date +%s)
APPLY_SECS=$((APPLY_END - APPLY_START))
echo -e "\n${GREEN}✓ Apply completado en ${APPLY_SECS}s${NC}"

# ─── Obtener URL del output ───────────────────────────────────────────────────
URL=""
if terraform output "$OUTPUT_URL_KEY" &>/dev/null 2>&1; then
  RAW_URL=$(terraform output -raw "$OUTPUT_URL_KEY" 2>/dev/null || echo "")
  if [[ -n "$RAW_URL" ]]; then
    URL="${URL_PREFIX}${RAW_URL}"
  fi
fi

echo -e "\n${BOLD}${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}  Stack desplegado — recursos activos y cobrando${NC}"
if [[ -n "$URL" ]]; then
  echo -e "${BOLD}  URL: ${GREEN}${URL}${NC}"
fi
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${NC}\n"

# ─── FASE 2: Ventana de capturas ──────────────────────────────────────────────
echo -e "${BOLD}${YELLOW}▶ FASE 2: Ventana para capturas y evidencia${NC}\n"
echo -e "Tienes ${BOLD}${TIMER_MINUTES} minutos${NC} para:"
echo -e "  1. Verificar que el servicio responde: ${GREEN}${URL:-'(ver outputs de terraform)'}${NC}"
echo -e "  2. Tomar screenshots de la consola AWS"
echo -e "  3. Copiar los nombres exactos de recursos (ARNs, IPs, etc.)"
echo -e "  4. Guardar las imágenes en ${BOLD}${CASO}/img/${NC} para el VISUALIZATION.md"
echo -e "\nEl destroy se ejecutara ${BOLD}automaticamente${NC} cuando:"
echo -e "  a) Presiones ${BOLD}ENTER${NC} para confirmar que terminaste, o"
echo -e "  b) Expire el timer de ${BOLD}${TIMER_MINUTES} minutos${NC}\n"

# Timer en background
TIMER_SECS=$((TIMER_MINUTES * 60))
DEADLINE=$(($(date +%s) + TIMER_SECS))

(
  sleep "$TIMER_SECS"
  echo -e "\n${RED}${BOLD}⏰ TIEMPO EXPIRADO — iniciando terraform destroy automatico...${NC}"
  # Matar el proceso de espera del usuario si sigue activo
  kill -SIGUSR1 $$ 2>/dev/null || true
) &
TIMER_PID=$!

# Trap para manejar el timer o Ctrl+C
destroy_cleanup() {
  kill "$TIMER_PID" 2>/dev/null || true
  echo -e "\n${YELLOW}Iniciando destroy por señal externa...${NC}"
}
trap destroy_cleanup SIGUSR1 SIGINT SIGTERM

# Mostrar countdown en segundos mientras esperamos input
show_countdown() {
  local remaining
  while true; do
    remaining=$((DEADLINE - $(date +%s)))
    if [[ $remaining -le 0 ]]; then break; fi
    printf "\r${CYAN}Tiempo restante: %02d:%02d  (ENTER para destroy ahora)${NC}" \
      $((remaining / 60)) $((remaining % 60))
    sleep 5
  done
}

show_countdown &
COUNTDOWN_PID=$!

# Esperar input del usuario o señal del timer
read -r -t "$TIMER_SECS" USER_INPUT || true

kill "$COUNTDOWN_PID" 2>/dev/null || true
kill "$TIMER_PID" 2>/dev/null || true
echo ""

# ─── FASE 3: Terraform Destroy ────────────────────────────────────────────────
echo -e "\n${BOLD}${RED}▶ FASE 3: terraform destroy${NC}"
echo -e "${YELLOW}Destruyendo todos los recursos de $CASO_NOMBRE...${NC}\n"

DESTROY_START=$(date +%s)
terraform destroy -auto-approve -no-color
DESTROY_END=$(date +%s)
DESTROY_SECS=$((DESTROY_END - DESTROY_START))

# ─── RESUMEN FINAL ────────────────────────────────────────────────────────────
TOTAL_SECS=$((DESTROY_END - APPLY_START))
COST_EST=""
if [[ "$CASO" == "caso-j" ]]; then
  # Fargate 0.25vCPU + ALB: ~$0.02012/min
  COST_EST=$(python3 -c "print(f'\${($TOTAL_SECS/60)*0.02012:.4f}')" 2>/dev/null || echo "< \$1")
elif [[ "$CASO" == "caso-k" ]]; then
  # EKS CP $0.10/hr + NAT GW $0.045/hr = $0.145/hr = $0.00242/min
  COST_EST=$(python3 -c "print(f'\${($TOTAL_SECS/60)*0.00242:.4f}')" 2>/dev/null || echo "< \$1")
fi

echo -e "\n${BOLD}${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${GREEN}  GameDay completado — recursos destruidos${NC}"
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "  Apply:     ${APPLY_SECS}s"
echo -e "  Ventana:   $((TOTAL_SECS - APPLY_SECS - DESTROY_SECS))s"
echo -e "  Destroy:   ${DESTROY_SECS}s"
echo -e "  Total:     ${TOTAL_SECS}s ($((TOTAL_SECS/60)) min)"
if [[ -n "$COST_EST" ]]; then
  echo -e "  Costo est: ${COST_EST} USD"
fi
echo -e ""
echo -e "${CYAN}Proximos pasos:${NC}"
echo -e "  1. Revisa las capturas en ${CASO}/img/"
echo -e "  2. Actualiza ${CASO}/VISUALIZATION.md con las evidencias"
echo -e "  3. Ejecuta: /visualizacion-evidencia ${CASO}"
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${NC}\n"
