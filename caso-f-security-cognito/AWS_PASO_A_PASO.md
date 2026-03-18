# AWS Paso a Paso — Caso F: Security First

## Prerequisitos

- AWS CLI configurado (`aws configure`)
- AWS SAM CLI instalado (`sam --version`)
- Python 3.12+ (para tests locales)
- Permisos IAM: `cognito-idp:*`, `lambda:*`, `apigateway:*`, `wafv2:*`, `iam:CreateRole`, `cloudformation:*`

---

## Paso 1: Entender la estructura

```
caso-f-security-cognito/
├── backend/
│   ├── template.yaml          # SAM: Cognito + HttpApi + Lambda + WAF
│   ├── src/
│   │   └── app.py             # Handler + pre_signup_trigger
│   ├── events/
│   │   ├── register.json      # Evento de prueba local
│   │   └── login.json
│   └── tests/
│       ├── conftest.py
│       └── test_app.py        # 35+ tests unitarios
├── index.html                 # Landing estática (misma que sirve la Lambda)
├── docs/
│   └── architecture.md        # Diagrama Mermaid
├── README.md
└── AWS_PASO_A_PASO.md         # (este archivo)
```

---

## Paso 2: Ejecutar tests unitarios

```bash
cd caso-f-security-cognito
pip install pytest boto3
pytest backend/tests/ -v --tb=short
```

Todos los tests usan `unittest.mock.patch` — no necesitan credenciales AWS.

---

## Paso 3: Invocar la Lambda localmente (opcional)

```bash
cd backend
sam build

# Prueba el endpoint de registro (falla si no hay Cognito real, útil para ver el routing)
sam local invoke SecurityFunction -e events/register.json

# Prueba la landing page
sam local start-api
# Luego abre http://localhost:3000
```

---

## Paso 4: Desplegar en AWS

```bash
cd backend

# Primera vez — configura el nombre del stack, región y S3 para artefactos
sam build && sam deploy --guided
```

Responde a las preguntas:
- **Stack Name**: `caso-f-security-cognito`
- **AWS Region**: `us-east-2` (o tu región)
- **DeployWAF**: `false` (recomendado para demo)
- **Confirm changes**: `y`
- **Allow SAM CLI IAM role creation**: `y`
- **Save arguments to samconfig.toml**: `y`

---

## Paso 5: Obtener las URLs

Al terminar el deploy, SAM muestra los Outputs:

```
Outputs:
  ApiBaseUrl       = https://xxxx.execute-api.us-east-2.amazonaws.com
  UserPoolId       = us-east-2_XXXXXXX
  UserPoolClientId = 1234567890abcdefghijklmn
  FunctionName     = caso-f-security-cognito-SecurityFunction-XXXX
```

---

## Paso 6: Probar manualmente con curl

```bash
export API_F_URL=https://xxxx.execute-api.us-east-2.amazonaws.com

# 1. Registrar usuario
curl -s -X POST "$API_F_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq .

# 2. Hacer login y guardar token
TOKEN=$(curl -s -X POST "$API_F_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq -r '.accessToken')

# 3. Llamar endpoint protegido con JWT
curl -s "$API_F_URL/profile" \
  -H "Authorization: $TOKEN" | jq .

# 4. Verificar que /profile rechaza requests sin token (403)
curl -s -o /dev/null -w "%{http_code}" "$API_F_URL/profile"
```

---

## Paso 7: Ejecutar smoke test automatizado

```bash
export API_F_URL=https://xxxx.execute-api.us-east-2.amazonaws.com
bash scripts/smoke/smoke_caso_f.sh
```

---

## Paso 8: Demo visual

Abre `$API_F_URL` en el navegador. La landing page sirve la interfaz interactiva de 3 pasos: registrar → login → perfil.

---

## Paso 9: Activar WAF (opcional)

```bash
# Solo si quieres probar el perimetro (~$5 USD/mes)
sam deploy --parameter-overrides DeployWAF=true
```

Para verificar que WAF bloquea SQLi:
```bash
curl -s "$API_F_URL/auth/login?q=1' OR '1'='1" -w "\nHTTP: %{http_code}\n"
# Esperado: HTTP 403 (bloqueado por WAF antes de llegar a Lambda)
```

---

## Paso 10: Limpiar todo

```bash
cd backend
sam delete --stack-name caso-f-security-cognito
```

> Esto elimina: Lambda, API Gateway, Cognito User Pool (y todos sus usuarios), WAF (si fue desplegado), roles IAM y CloudFormation stack.

---

## Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `NotAuthorizedException` en login | Credenciales incorrectas | Verificar email/password |
| `InvalidParameterException` | Password no cumple política | Mínimo 8 chars, mayúscula, número |
| `403` en `/profile` sin token | JWT Authorizer rechaza la request | Incluir `Authorization: <access_token>` en el header |
| `UserPoolClient does not support USER_PASSWORD_AUTH` | App Client sin el flujo habilitado | SAM template ya lo incluye; asegurarse de hacer `sam deploy` fresco |
| WAF `403` en requests legítimas | False positive en AWSManagedRulesCommonRuleSet | Revisar WAF logs en CloudWatch; considerar `Count` mode en lugar de `Block` |
