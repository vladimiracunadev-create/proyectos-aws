#!/usr/bin/env bash
# Smoke test Caso E — DynamoDB Persistence Pro
# Requiere: API_E_URL
set -euo pipefail

BASE="${API_E_URL:?La variable API_E_URL no está definida}"
echo "=== Smoke Caso E: ${BASE} ==="

echo "--- POST /orders ---"
STATUS=$(curl -s -o /tmp/smoke_e_post.json -w "%{http_code}" -X POST "${BASE}/orders" \
  -H "Content-Type: application/json" \
  -d '{"customerId":"smoke-ci-001","customerName":"Smoke CI","productId":"prod-smoke","productName":"Smoke Product","total":1.00,"status":"PENDING"}')

echo "HTTP ${STATUS}"
cat /tmp/smoke_e_post.json
[ "$STATUS" = "201" ] || { echo "FAIL POST /orders: esperado 201, recibido ${STATUS}"; exit 1; }
grep -q '"ok":true' /tmp/smoke_e_post.json || { echo "FAIL: campo ok:true ausente en POST"; exit 1; }

echo "--- GET /customers/smoke-ci-001/orders ---"
STATUS=$(curl -s -o /tmp/smoke_e_get_cust.json -w "%{http_code}" \
  "${BASE}/customers/smoke-ci-001/orders")
echo "HTTP ${STATUS}"
[ "$STATUS" = "200" ] || { echo "FAIL GET customer orders: esperado 200, recibido ${STATUS}"; exit 1; }

echo "--- GET /orders/status/PENDING ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${BASE}/orders/status/PENDING")
[ "$STATUS" = "200" ] || { echo "FAIL GET status: esperado 200, recibido ${STATUS}"; exit 1; }

echo "--- GET /products/prod-smoke/orders ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${BASE}/products/prod-smoke/orders")
[ "$STATUS" = "200" ] || { echo "FAIL GET product: esperado 200, recibido ${STATUS}"; exit 1; }

echo "PASS Caso E"
