#!/usr/bin/env bash
# =============================================================================
# check.sh — Verificador de endpoint y estado de resiliencia
# Caso M: Resiliencia & Failover
#
# Estado: PLACEHOLDER — Activo en Fase 1+
# Este script valida que el endpoint responde correctamente y detecta la AZ/región
# desde la que responde. Se usa como baseline antes y durante el GameDay.
#
# Uso:
#   ./scripts/check.sh                     # Check único
#   ./scripts/check.sh --continuous        # Check cada 5 segundos (modo watch)
#   ./scripts/check.sh --endpoint <URL>    # Override del endpoint
# =============================================================================

set -euo pipefail

# ─── Configuración (actualizar en Fase 1) ────────────────────────────────────
ENDPOINT="${ENDPOINT:-https://PLACEHOLDER_ALB_DNS/healthz}"
INTERVAL="${INTERVAL:-5}"
MAX_FAILURES="${MAX_FAILURES:-3}"
# ─────────────────────────────────────────────────────────────────────────────

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC}    $(date '+%H:%M:%S') $*"; }
log_fail() { echo -e "${RED}[FAIL]${NC}  $(date '+%H:%M:%S') $*"; }
log_info() { echo -e "${YELLOW}[INFO]${NC}  $(date '+%H:%M:%S') $*"; }

check_endpoint() {
  local url="$1"
  local http_code
  local body

  # ── PLACEHOLDER: En Fase 1 este bloque estará activo ──────────────────────
  # http_code=$(curl -s -o /tmp/caso_m_response.json -w "%{http_code}" \
  #   --max-time 5 --retry 1 "$url")
  # body=$(cat /tmp/caso_m_response.json 2>/dev/null || echo "{}")
  # ──────────────────────────────────────────────────────────────────────────

  # Simulación para Fase 0 (placeholder)
  log_info "[FASE 0 — PLACEHOLDER] El endpoint '$url' no está activo todavía."
  log_info "En Fase 1, este script verifica: HTTP 200, campo 'status', campo 'region' y 'az'."
  log_info "Ejemplo de respuesta esperada:"
  echo '  {"status":"healthy","region":"us-east-1","az":"us-east-1a","timestamp":"2026-01-01T00:00:00Z"}'
  return 0
}

run_single_check() {
  log_info "Verificando endpoint: $ENDPOINT"
  if check_endpoint "$ENDPOINT"; then
    log_ok "Check pasado. El sistema responde correctamente."
  else
    log_fail "El endpoint no respondi\u00f3. Ver detalles arriba."
    exit 1
  fi
}

run_continuous() {
  local failures=0
  log_info "Modo continuo activado. Intervalo: ${INTERVAL}s. Max failures: ${MAX_FAILURES}"
  log_info "Presiona Ctrl+C para detener."

  while true; do
    if check_endpoint "$ENDPOINT"; then
      log_ok "Check OK (failures consecutivos: $failures)"
      failures=0
    else
      ((failures++))
      log_fail "Failure #${failures}/${MAX_FAILURES}"
      if [[ $failures -ge $MAX_FAILURES ]]; then
        log_fail "Se superó el umbral de failures. El sistema no está respondiendo."
        exit 1
      fi
    fi
    sleep "$INTERVAL"
  done
}

# ─── Argparse simple ─────────────────────────────────────────────────────────
CONTINUOUS=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --continuous) CONTINUOUS=true ;;
    --endpoint)   ENDPOINT="$2"; shift ;;
    --interval)   INTERVAL="$2"; shift ;;
    -h|--help)
      echo "Uso: $0 [--continuous] [--endpoint URL] [--interval SEGUNDOS]"
      exit 0
      ;;
  esac
  shift
done

echo "============================================================"
echo " Caso M: Resiliencia & Failover — Health Check Script"
echo " [PLACEHOLDER — Fase 0]"
echo "============================================================"

if $CONTINUOUS; then
  run_continuous
else
  run_single_check
fi
