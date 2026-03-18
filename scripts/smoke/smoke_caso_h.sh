#!/usr/bin/env bash
# Smoke test Caso H — Observability (CloudWatch + X-Ray)
# Requiere: API_H_URL
set -euo pipefail

BASE="${API_H_URL:?La variable API_H_URL no está definida}"
echo "=== Smoke Caso H: ${BASE} ==="

echo "--- GET /health?format=json ---"
STATUS=$(curl -s -o /tmp/smoke_h_health.json -w "%{http_code}" "${BASE}/health?format=json")
echo "HTTP ${STATUS}"
cat /tmp/smoke_h_health.json
[ "$STATUS" = "200" ] || { echo "FAIL GET /health: esperado 200, recibido ${STATUS}"; exit 1; }
grep -q '"xray"' /tmp/smoke_h_health.json || { echo "FAIL: campo xray ausente en health"; exit 1; }
grep -q '"metricNamespace"' /tmp/smoke_h_health.json || { echo "FAIL: campo metricNamespace ausente"; exit 1; }

echo "--- POST /metrics ---"
STATUS=$(curl -s -o /tmp/smoke_h_metrics.json -w "%{http_code}" -X POST "${BASE}/metrics")
echo "HTTP ${STATUS}"
cat /tmp/smoke_h_metrics.json
[ "$STATUS" = "200" ] || { echo "FAIL POST /metrics: esperado 200, recibido ${STATUS}"; exit 1; }
grep -q '"namespace"' /tmp/smoke_h_metrics.json || { echo "FAIL: campo namespace ausente"; exit 1; }

echo "PASS Caso H"
