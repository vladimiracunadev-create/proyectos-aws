#!/usr/bin/env bash
# Smoke test Caso G — Event Driven (EventBridge + SQS)
# Requiere: API_G_URL
set -euo pipefail

BASE="${API_G_URL:?La variable API_G_URL no está definida}"
echo "=== Smoke Caso G: ${BASE} ==="

echo "--- GET /health (JSON) ---"
STATUS=$(curl -s -o /tmp/smoke_g_health.json -w "%{http_code}" \
  -H "Accept: application/json" "${BASE}/health")
echo "HTTP ${STATUS}"
cat /tmp/smoke_g_health.json
[ "$STATUS" = "200" ] || { echo "FAIL GET /health: esperado 200, recibido ${STATUS}"; exit 1; }
grep -q '"status"' /tmp/smoke_g_health.json || { echo "FAIL: campo status ausente en health"; exit 1; }
grep -q '"eventBus"' /tmp/smoke_g_health.json || { echo "FAIL: campo eventBus ausente en health"; exit 1; }

echo "--- POST /events/orders ---"
STATUS=$(curl -s -o /tmp/smoke_g_event.json -w "%{http_code}" -X POST "${BASE}/events/orders" \
  -H "Content-Type: application/json" \
  -d '{"customerId":"smoke-ci-001","customerName":"Smoke CI","status":"CREATED","total":1.00}')
echo "HTTP ${STATUS}"
cat /tmp/smoke_g_event.json
[ "$STATUS" = "202" ] || { echo "FAIL POST /events/orders: esperado 202, recibido ${STATUS}"; exit 1; }
grep -q '"eventId"' /tmp/smoke_g_event.json || { echo "FAIL: campo eventId ausente en respuesta"; exit 1; }

echo "PASS Caso G"
