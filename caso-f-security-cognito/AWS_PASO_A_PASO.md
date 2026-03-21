# AWS Paso a Paso - Caso F

## Antes de empezar

Necesitas:

- AWS CLI configurado
- AWS SAM CLI instalado
- Python 3.12+
- permisos para Cognito, Lambda, API Gateway, CloudFormation y WAF

## Como leer este caso

No intentes entenderlo como "dos productos". Leelo asi:

1. `DEMO`: demuestra identidad y autorizacion
2. pagina WAF: demuestra la capa perimetral usando la misma identidad del `DEMO`
3. `VISUALIZATION.md`: documenta evidencia y cierre FinOps

## Paso 1: Ejecutar tests

```bash
python -m pytest caso-f-security-cognito/backend/tests/ -v --tb=short
```

## Paso 2: Desplegar el DEMO principal

```bash
cd caso-f-security-cognito/backend
sam build
sam deploy --guided
```

Valores sugeridos:

- `Stack Name`: `caso-f-security-cognito`
- `AWS Region`: `us-east-2`
- `Allow SAM CLI IAM role creation`: `y`

## Paso 3: Recuperar outputs reales del DEMO

```bash
aws cloudformation describe-stacks \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --query "Stacks[0].Outputs"
```

Debes guardar:

- `ApiBaseUrl`
- `UserPoolId`
- `UserPoolArn`
- `UserPoolClientId`

## Paso 4: Entender que demuestra el DEMO

Abre la URL `ApiBaseUrl` en el navegador.

La landing debe responderle a un novato estas preguntas:

- que estoy viendo
- que estamos haciendo
- para que sirve
- que gano con esta arquitectura
- que problema estoy resolviendo

Luego ejecuta el flujo:

1. registrar usuario
2. iniciar sesion
3. copiar el `idToken`
4. llamar a `/profile`

Cuando `/profile` devuelve `200`, ya demostraste:

- identidad real
- token real
- authorizer nativo
- Lambda sin validacion criptografica manual

## Paso 5: Desplegar la pagina WAF usando la misma identidad del DEMO

La pagina WAF no crea otro usuario. Reutiliza la identidad del `DEMO`.

```bash
cd caso-f-security-cognito/backend
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    DemoPageUrl=https://<demo-url> \
    ExistingUserPoolArn=arn:aws:cognito-idp:us-east-2:<account-id>:userpool/<user-pool-id> \
    ExistingUserPoolId=<user-pool-id> \
    ExistingUserPoolClientId=<client-id>
```

## Paso 6: Volver a desplegar el DEMO con el enlace WAF

```bash
cd caso-f-security-cognito/backend
sam deploy \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SupportPageUrl=https://<waf-url>
```

## Paso 7: Probar la relacion entre DEMO y WAF

Abre la pagina WAF auxiliar.

La lectura correcta es esta:

- en el `DEMO` probaste "quien eres"
- aqui pruebas "que solicitudes se frenan antes de entrar"
- el token debe ser el mismo

Haz estas tres pruebas:

1. `GET /health`
2. `GET /profile` pegando el mismo `idToken` del `DEMO`
3. `GET /health?filter=1%27%20or%201%3D1%20--`

Esperado:

- `200` en `GET /health`
- `200` en `GET /profile` con el mismo token
- `403` en la prueba SQLi controlada

## Paso 8: Menus AWS en ingles y espanol

AWS puede mostrar nombres distintos segun idioma. Usa esta tabla de traduccion:

| AWS Console (EN) | Referencia ES | Que revisar |
|---|---|---|
| `CloudFormation > Stacks` | `CloudFormation > Pilas` | stacks del `DEMO` y de la pagina WAF |
| `API Gateway > APIs` | `API Gateway > API` | una `HTTP API` para el `DEMO` y una `REST API` para WAF |
| `API Gateway > Routes` | `API Gateway > Rutas` | rutas del `DEMO` y la ruta protegida `/profile` del stack WAF |
| `API Gateway > Authorizers` | `API Gateway > Autorizadores` | `JWT Authorizer` en `HTTP API` y `Cognito Authorizer` en `REST API` |
| `Amazon Cognito > User pools` | `Amazon Cognito > Pools de usuarios` | el mismo `User Pool` reutilizado por ambos despliegues |
| `AWS WAF & Shield > Web ACLs` | `AWS WAF y Shield > Web ACLs` | asociacion del `Web ACL` al `REST API` |
| `Lambda > Functions` | `Lambda > Funciones` | funciones del caso |

## Paso 9: Nota importante si usas PowerShell

En Windows PowerShell, `curl` suele ser alias de `Invoke-WebRequest`.

Si un comando con `curl -X` falla, usa:

```powershell
curl.exe "https://<url>"
```

o bien:

```powershell
Invoke-RestMethod "https://<url>"
```

## Paso 10: Validacion por script

### DEMO

```bash
export API_F_URL=https://<demo-url>
bash scripts/smoke/smoke_caso_f.sh
```

### Pagina WAF

```bash
export API_F_URL=https://<waf-url>
export CASE_F_MODE=waf
export DEMO_ID_TOKEN=<id-token-del-demo>
export EXPECT_WAF=true
bash scripts/smoke/smoke_caso_f.sh
```

## Paso 11: Cerrar solo la ventana WAF

Cuando ya terminaste las capturas y pruebas perimetrales:

```bash
cd caso-f-security-cognito/backend
sam delete --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --no-prompts
```

El `DEMO` puede quedar vivo.
