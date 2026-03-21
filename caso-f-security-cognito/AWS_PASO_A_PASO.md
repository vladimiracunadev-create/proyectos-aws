# AWS Paso a Paso - Caso F: Security First

## Prerequisitos

- AWS CLI configurado (`aws configure`)
- AWS SAM CLI instalado (`sam --version`)
- Python 3.12+
- Permisos IAM para Cognito, Lambda, API Gateway, CloudFormation y WAF

## Estructura del caso

```text
caso-f-security-cognito/
|-- backend/
|   |-- template.yaml                # DEMO: HTTP API + JWT Authorizer
|   |-- template-visualization.yaml  # VISUALIZATION: REST API + WAF
|   |-- src/app.py                   # Handler compatible con ambos formatos
|   |-- events/
|   `-- tests/
|-- docs/architecture.md
|-- VISUALIZATION.md
|-- README.md
`-- index.html
```

## Paso 1: Ejecutar tests unitarios

```bash
python -m pytest caso-f-security-cognito/backend/tests/ -v --tb=short
```

Los tests cubren:

- routing HTTP API
- routing REST API
- register y login
- profile con claims inyectados
- health con metadata de modalidad

## Paso 2: Probar localmente la modalidad DEMO

```bash
cd caso-f-security-cognito/backend
sam build
sam local start-api
```

Abre [http://localhost:3000](http://localhost:3000) y prueba el flujo visual.

## Paso 3: Desplegar la modalidad DEMO

```bash
cd caso-f-security-cognito/backend
sam build
sam deploy --guided
```

Respuestas sugeridas:

- `Stack Name`: `caso-f-security-cognito`
- `AWS Region`: `us-east-2`
- `Confirm changes`: `y`
- `Allow SAM CLI IAM role creation`: `y`
- `Save arguments to samconfig.toml`: `y`

Outputs esperados:

```text
ApiBaseUrl       = https://xxxx.execute-api.us-east-2.amazonaws.com
UserPoolId       = us-east-2_XXXXXXX
UserPoolClientId = 1234567890abcdefghijklmn
FunctionName     = caso-f-security-cognito-SecurityFunction-XXXX
DeploymentMode   = demo-http-jwt
```

## Paso 4: Validar la modalidad DEMO con curl

```bash
export API_F_URL=https://xxxx.execute-api.us-east-2.amazonaws.com

# Registrar usuario
curl -s -X POST "$API_F_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq .

# Login y guardar ID token
TOKEN=$(curl -s -X POST "$API_F_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq -r '.idToken')

# Perfil protegido
curl -s "$API_F_URL/profile" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Sin token debe fallar con 401 o 403 segun authorizer
curl -s -o /dev/null -w "%{http_code}" "$API_F_URL/profile"
```

## Paso 5: Ejecutar smoke test

```bash
export API_F_URL=https://xxxx.execute-api.us-east-2.amazonaws.com
bash scripts/smoke/smoke_caso_f.sh
```

## Paso 6: Desplegar la modalidad VISUALIZATION

Esta modalidad existe porque AWS WAF se asocia a REST API, no a HTTP API.

```bash
cd caso-f-security-cognito/backend
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM
```

Outputs esperados:

```text
ApiBaseUrl       = https://xxxx.execute-api.us-east-2.amazonaws.com/Prod
UserPoolId       = us-east-2_XXXXXXX
UserPoolClientId = 1234567890abcdefghijklmn
FunctionName     = caso-f-security-cognito-visualization-SecurityFunction-XXXX
WebAclArn        = arn:aws:wafv2:...
DeploymentMode   = visualization-rest-waf
```

## Paso 7: Validar WAF de verdad

```bash
export API_F_URL=https://xxxx.execute-api.us-east-2.amazonaws.com/Prod
EXPECT_WAF=true bash scripts/smoke/smoke_caso_f.sh
```

Chequeo manual puntual:

```bash
curl -s "$API_F_URL/auth/login?q=1' OR '1'='1" -w "\nHTTP: %{http_code}\n"
```

Esperado:

- `HTTP 403`
- el request no debe llegar a la Lambda

## Paso 8: Capturar evidencia

Usa [VISUALIZATION.md](VISUALIZATION.md) como checklist para:

- stack desplegado
- authorizer funcionando
- WAF asociado
- login correcto
- `/profile` correcto
- SQLi de prueba bloqueado

## Paso 9: Limpiar

```bash
# Demo
sam delete --stack-name caso-f-security-cognito --region us-east-2

# Visualization
sam delete --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2
```

## Troubleshooting

| Problema | Causa probable | Solucion |
|---|---|---|
| `NotAuthorizedException` | Password o email incorrectos | Revisa credenciales |
| `InvalidParameterException` | Password no cumple politica | Minimo 8 chars, mayuscula y numero |
| `/profile` devuelve 401 o 403 | Falta token o token invalido | Usa `Authorization: Bearer <idToken>` |
| WAF no bloquea la prueba | Estas en DEMO o usando URL sin `/Prod` | Usa `template-visualization.yaml` y la URL correcta |
| La landing falla en REST API | URL base incompleta | Usa el `ApiBaseUrl` del output, incluyendo `/Prod` |
