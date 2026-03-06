#!/usr/bin/env bash
# =============================================================================
# drill-failover.sh — Simulación de Failover (GameDay)
# Caso M: Resiliencia & Failover
#
# Estado: PLACEHOLDER — Activo en Fase 2+
# Este script simula un fallo para demostrar el failover automático.
# Es NO DESTRUCTIVO en Fase 0: solo muestra los comandos que ejecutaría.
#
# PARA ACTIVAR: comentar el bloque "DRY RUN" y descomentar los comandos reales.
#
# Uso:
#   ./scripts/drill-failover.sh --mode task      # Bajar 1 task ECS (Fase 1)
#   ./scripts/drill-failover.sh --mode az        # Simular caída de AZ (Fase 1)
#   ./scripts/drill-failover.sh --mode regional  # Caída regional (Fase 2)
# =============================================================================

set -euo pipefail

# ─── Configuración (actualizar en Fase 1) ────────────────────────────────────
ECS_CLUSTER="${ECS_CLUSTER:-PLACEHOLDER_CLUSTER_NAME}"
ECS_SERVICE="${ECS_SERVICE:-PLACEHOLDER_SERVICE_NAME}"
TARGET_GROUP_ARN="${TARGET_GROUP_ARN:-PLACEHOLDER_TARGET_GROUP_ARN}"
PRIMARY_REGION="${PRIMARY_REGION:-us-east-1}"
# ─────────────────────────────────────────────────────────────────────────────

YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_warn() { echo -e "${YELLOW}[WARN]${NC}  $(date '+%H:%M:%S') $*"; }
log_dry()  { echo -e "${RED}[DRY-RUN]${NC} $(date '+%H:%M:%S') [NO EJECUTADO] $*"; }

MODE="${1:-}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="$2"; shift ;;
    -h|--help)
      echo "Uso: $0 --mode [task|az|regional]"
      exit 0
      ;;
  esac
  shift
done

echo "=================================================================="
echo " Caso M: Resiliencia & Failover — Drill de Failover (GameDay)"
echo " [PLACEHOLDER — Fase 0 — MODO SECO: ningún comando se ejecuta]"
echo "=================================================================="

case "${MODE}" in
  task)
    log_warn "Modo: Caída de 1 Task ECS (Fase 1)"
    log_dry "aws ecs list-tasks --cluster ${ECS_CLUSTER} --query 'taskArns[0]' --output text"
    log_dry "aws ecs stop-task --cluster ${ECS_CLUSTER} --task <TASK_ARN> --reason 'GameDay: drill'"
    log_dry "# Observar: aws elbv2 describe-target-health --target-group-arn ${TARGET_GROUP_ARN}"
    ;;

  az)
    log_warn "Modo: Simulación de caída de AZ (Fase 1 avanzado)"
    log_dry "aws elbv2 deregister-targets --target-group-arn ${TARGET_GROUP_ARN} --targets Id=<INSTANCE_AZ_A>"
    log_dry "# Observar: watch -n 5 'aws elbv2 describe-target-health ...'"
    ;;

  regional)
    log_warn "Modo: Caída Regional — Route 53 Failover (Fase 2)"
    log_dry "aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE} --desired-count 0"
    log_dry "# Observar: watch -n 10 'dig +short <API_DOMAIN>'"
    log_dry "# Esperar cambio de IP (~60-120 segundos TTL Route 53)"
    ;;

  *)
    echo "ERROR: Modo no especificado o inválido."
    echo "Uso: $0 --mode [task|az|regional]"
    exit 1
    ;;
esac

echo ""
log_warn "RECORDATORIO: Ejecutar './scripts/drill-failback.sh' para restaurar el sistema."
echo "Ver runbook completo en: docs/runbook-failover.md"
