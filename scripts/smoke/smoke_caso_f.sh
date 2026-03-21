#!/usr/bin/env bash
# Smoke test - Caso F: Security First (Cognito + Authorizer nativo + WAF)
# Requiere: API_F_URL
# Modo DEMO (default): TEST_EMAIL y TEST_PASSWORD opcionales
# Modo WAF: CASE_F_MODE=waf y DEMO_ID_TOKEN obligatorio
# Opcional: EXPECT_WAF=true para validar bloqueo SQLi

set -euo pipefail

BASE="${API_F_URL:?La variable API_F_URL no esta definida}"
MODE="${CASE_F_MODE:-demo}"
EMAIL="${TEST_EMAIL:-smoketest_$(date +%s)@demo.com}"
PASSWORD="${TEST_PASSWORD:-SmokeTest1!}"

PASS=0
FAIL=0

check() {
  local desc="$1" expected="$2" actual="$3"
  if [ "$actual" = "$expected" ]; then
    echo "  [OK]  $desc (HTTP $actual)"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $desc - esperado HTTP $expected, obtenido HTTP $actual"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Smoke Test: Caso F ==="
echo "Base URL: $BASE"
echo "Modo: $MODE"
[ "$MODE" = "demo" ] && echo "Email: $EMAIL"
echo ""

# 1. Landing page
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/")
check "GET / devuelve landing HTML" "200" "$STATUS"

# 2. Health check
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/health")
check "GET /health devuelve 200" "200" "$STATUS"

HEALTH=$(curl -s "$BASE/health")
if echo "$HEALTH" | grep -q '"status"'; then
  echo "  [OK]  GET /health contiene campo 'status'"
  PASS=$((PASS + 1))
else
  echo "  [FAIL] GET /health no contiene campo 'status'"
  FAIL=$((FAIL + 1))
fi

# 3. /profile sin token debe devolver 401 o 403 segun el authorizer
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/profile")
if [ "$STATUS" = "401" ] || [ "$STATUS" = "403" ]; then
  echo "  [OK]  GET /profile sin token devuelve $STATUS"
  PASS=$((PASS + 1))
else
  echo "  [FAIL] GET /profile sin token esperaba 401/403, obtuvo HTTP $STATUS"
  FAIL=$((FAIL + 1))
fi

# 4+. Flujo DEMO o flujo WAF segun modo
if [ "$MODE" = "demo" ]; then
  REGISTER_BODY=$(curl -s -X POST "$BASE/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
  REGISTER_STATUS=$(echo "$REGISTER_BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok' if d.get('ok') else 'fail')" 2>/dev/null || echo "fail")

  if [ "$REGISTER_STATUS" = "ok" ]; then
    echo "  [OK]  POST /auth/register crea usuario"
    PASS=$((PASS + 1))
  else
    if echo "$REGISTER_BODY" | grep -q "UsernameExistsException\|ya existe"; then
      echo "  [OK]  POST /auth/register (usuario ya existe - re-run OK)"
      PASS=$((PASS + 1))
    else
      echo "  [FAIL] POST /auth/register - respuesta: $REGISTER_BODY"
      FAIL=$((FAIL + 1))
    fi
  fi
  
  LOGIN_RESP=$(curl -s -X POST "$BASE/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
  PROFILE_TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('idToken') or d.get('accessToken',''))" 2>/dev/null || echo "")

  if [ -n "$PROFILE_TOKEN" ]; then
    echo "  [OK]  POST /auth/login devuelve token util para /profile"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] POST /auth/login no devolvio token util - respuesta: $LOGIN_RESP"
    FAIL=$((FAIL + 1))
  fi
else
  PROFILE_TOKEN="${DEMO_ID_TOKEN:-}"
  if [ -n "$PROFILE_TOKEN" ]; then
    echo "  [OK]  DEMO_ID_TOKEN recibido para probar la capa WAF"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] En modo WAF debes definir DEMO_ID_TOKEN con el idToken del DEMO"
    FAIL=$((FAIL + 1))
  fi
fi

if [ -n "$PROFILE_TOKEN" ]; then
  PROFILE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/profile" \
    -H "Authorization: Bearer $PROFILE_TOKEN")
  check "GET /profile con token valido devuelve 200" "200" "$PROFILE_STATUS"

  PROFILE_BODY=$(curl -s "$BASE/profile" -H "Authorization: Bearer $PROFILE_TOKEN")
  if echo "$PROFILE_BODY" | grep -q '"email"'; then
    echo "  [OK]  GET /profile devuelve claims con campo 'email'"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] GET /profile no devolvio campo 'email' - respuesta: $PROFILE_BODY"
    FAIL=$((FAIL + 1))
  fi
fi

# 7. Validacion WAF opcional
if [ "${EXPECT_WAF:-false}" = "true" ]; then
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/health?filter=1'%20OR%201%3D1%20--")
  check "WAF bloquea payload SQLi de prueba" "403" "$STATUS"
fi

# 8. Ruta inexistente
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/no-existe")
check "GET /no-existe devuelve 404" "404" "$STATUS"

echo ""
echo "=== Resultado: $PASS OK, $FAIL FAIL ==="
[ $FAIL -eq 0 ] && exit 0 || exit 1
