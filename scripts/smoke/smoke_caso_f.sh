#!/usr/bin/env bash
# Smoke test — Caso F: Security First (Cognito + JWT)
# Requiere: API_F_URL, TEST_EMAIL (opcional), TEST_PASSWORD (opcional)

set -euo pipefail

BASE="${API_F_URL:?La variable API_F_URL no está definida}"
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
    echo "  [FAIL] $desc — esperado HTTP $expected, obtenido HTTP $actual"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Smoke Test: Caso F ==="
echo "Base URL: $BASE"
echo "Email: $EMAIL"
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

# 3. /profile sin token debe devolver 403 (JWT Authorizer rechaza)
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/profile")
check "GET /profile sin token devuelve 403" "403" "$STATUS"

# 4. Registro de usuario
REGISTER_BODY=$(curl -s -X POST "$BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
REGISTER_STATUS=$(echo "$REGISTER_BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok' if d.get('ok') else 'fail')" 2>/dev/null || echo "fail")

if [ "$REGISTER_STATUS" = "ok" ]; then
  echo "  [OK]  POST /auth/register crea usuario"
  PASS=$((PASS + 1))
else
  # Puede ser 409 si el usuario ya existe (re-run del smoke test)
  if echo "$REGISTER_BODY" | grep -q "UsernameExistsException\|ya existe"; then
    echo "  [OK]  POST /auth/register (usuario ya existe — re-run OK)"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] POST /auth/register — respuesta: $REGISTER_BODY"
    FAIL=$((FAIL + 1))
  fi
fi

# 5. Login
LOGIN_RESP=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
ACCESS_TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('accessToken',''))" 2>/dev/null || echo "")

if [ -n "$ACCESS_TOKEN" ]; then
  echo "  [OK]  POST /auth/login devuelve accessToken"
  PASS=$((PASS + 1))
else
  echo "  [FAIL] POST /auth/login no devolvio accessToken — respuesta: $LOGIN_RESP"
  FAIL=$((FAIL + 1))
fi

# 6. /profile con token válido
if [ -n "$ACCESS_TOKEN" ]; then
  PROFILE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/profile" \
    -H "Authorization: $ACCESS_TOKEN")
  check "GET /profile con JWT válido devuelve 200" "200" "$PROFILE_STATUS"

  PROFILE_BODY=$(curl -s "$BASE/profile" -H "Authorization: $ACCESS_TOKEN")
  if echo "$PROFILE_BODY" | grep -q '"email"'; then
    echo "  [OK]  GET /profile devuelve claims con campo 'email'"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] GET /profile no devolvio campo 'email' — respuesta: $PROFILE_BODY"
    FAIL=$((FAIL + 1))
  fi
fi

# 7. Ruta inexistente
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/no-existe")
check "GET /no-existe devuelve 404" "404" "$STATUS"

# Resultado final
echo ""
echo "=== Resultado: $PASS OK, $FAIL FAIL ==="
[ $FAIL -eq 0 ] && exit 0 || exit 1
