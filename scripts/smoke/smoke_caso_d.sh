#!/usr/bin/env bash
# Smoke test Caso D — POST /lead
# Requiere: API_D_URL (ej: https://xxxx.execute-api.us-east-2.amazonaws.com)
set -euo pipefail

BASE="${API_D_URL:?La variable API_D_URL no está definida}"
echo "=== Smoke Caso D: ${BASE} ==="

echo "--- POST /lead (válido) ---"
STATUS=$(curl -s -o /tmp/smoke_d.json -w "%{http_code}" -X POST "${BASE}/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"Smoke Test CI","email":"smoke@ci.test","message":"Smoke test automatico desde CI"}')

echo "HTTP ${STATUS}"
cat /tmp/smoke_d.json
[ "$STATUS" = "200" ] || { echo "FAIL: esperado 200, recibido ${STATUS}"; exit 1; }
grep -q '"ok":true' /tmp/smoke_d.json || { echo "FAIL: campo ok:true ausente"; exit 1; }

echo "--- POST /lead (honeypot) ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE}/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"Bot","email":"b@b.com","message":"spam","company":"Bots Inc"}')
[ "$STATUS" = "200" ] || { echo "FAIL honeypot: esperado 200, recibido ${STATUS}"; exit 1; }

echo "PASS Caso D"
