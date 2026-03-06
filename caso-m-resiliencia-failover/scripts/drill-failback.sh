#!/usr/bin/env bash
# =============================================================================
# drill-failback.sh — Failback Controlado (GameDay)
# Caso M: Resiliencia & Failover
#
# Estado: PLACEHOLDER — Activo en Fase 2+
# Restaura el sistema al estado primario luego de un ejercicio de failover.
# SIEMPRE se ejecuta después de drill-failover.sh.
#
# Regla de oro: El failback es SIEMPRE manual y controlado, nunca automático.
# =============================================================================

set -euo pipefail

# ─── Configuración (actualizar en Fase 1) ────────────────────────────────────
ECS_CLUSTER="${ECS_CLUSTER:-PLACEHOLDER_CLUSTER_NAME}"
ECS_SERVICE="${ECS_SERVICE:-PLACEHOLDER_SERVICE_NAME}"
TARGET_GROUP_ARN="${TARGET_GROUP_ARN:-PLACEHOLDER_TARGET_GROUP_ARN}"
DESIRED_COUNT="${DESIRED_COUNT:-2}"
API_DOMAIN="${API_DOMAIN:-PLACEHOLDER_DOMAIN}"
# ─────────────────────────────────────────────────────────────────────────────

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC}    $(date '+%H:%M:%S') $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $(date '+%H:%M:%S') $*"; }
log_dry()  { echo -e "${RED}[DRY-RUN]${NC} $(date '+%H:%M:%S') [NO EJECUTADO] $*"; }

echo "=================================================================="
echo " Caso M: Resiliencia & Failover — Failback Controlado (GameDay)"
echo " [PLACEHOLDER — Fase 0 — MODO SECO: ningún comando se ejecuta]"
echo "=================================================================="

log_warn "Paso 1: Restaurar servicio ECS primario"
log_dry "aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE} --desired-count ${DESIRED_COUNT} --region us-east-1"

log_warn "Paso 2: Esperar que los targets vuelvan a healthy en ALB primario"
log_dry "aws elbv2 wait target-in-service --target-group-arn ${TARGET_GROUP_ARN}"

log_warn "Paso 3: Validar endpoint directo del ALB primario"
log_dry "curl -f http://PRIMARY_ALB_DNS/healthz"

log_warn "Paso 4: Esperar que Route 53 Health Check vuelva a verde (~30-60s)"
log_dry "aws route53 get-health-check-status --health-check-id <HC_ID>"

log_warn "Paso 5: Confirmar retorno DNS al primario"
log_dry "watch -n 10 'dig +short ${API_DOMAIN}'"

echo ""
log_ok "Script de failback completado (modo seco — Fase 0)."
log_ok "En Fase 2: descomentar los comandos reales y eliminar el flag dry-run."
echo "Ver documentación completa: docs/runbook-failover.md (Sección 5)"
