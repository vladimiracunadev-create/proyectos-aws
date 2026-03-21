# AWS Paso a Paso - Caso F: DEMO principal + pagina WAF auxiliar

## Antes de empezar

Necesitas:

- AWS CLI configurado
- AWS SAM CLI instalado
- Python 3.12+
- permisos para Lambda, API Gateway, Cognito, CloudFormation y WAF

## Modelo del caso

No hay dos productos. Hay tres piezas con roles distintos:

1. `DEMO`: producto principal y flujo completo
2. pagina WAF auxiliar: despliegue complementario enlazado desde el DEMO
3. `VISUALIZATION.md`: control de costo y destruccion segura

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

## Paso 3: Validar que el DEMO realmente funciona

Abre la URL del output `ApiBaseUrl`.

En la landing debes entender de inmediato:

- que estas viendo
- que estamos haciendo
- para que sirve
- que se gana
- que problema resuelve

Luego valida el flujo:

1. registrar usuario
2. iniciar sesion
3. llamar a `/profile`

## Paso 4: Desplegar la pagina WAF auxiliar

Esta URL existe para explicar y validar el perimetro. No reemplaza al DEMO.

```bash
cd caso-f-security-cognito/backend
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides DemoPageUrl=https://<demo-url>
```

## Paso 5: Enlazar el DEMO con la pagina WAF

Actualiza el DEMO para que muestre el enlace al despliegue WAF:

```bash
cd caso-f-security-cognito/backend
sam deploy \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SupportPageUrl=https://<waf-url>
```

## Paso 6: Validar la pagina WAF

Abre la URL del stack auxiliar.

La pagina debe dejar claro:

- por que existe este despliegue
- que resuelve el perimetro
- que prueba controlada puedes ejecutar
- que esta pagina es complementaria al DEMO

Luego valida:

```bash
curl -s "$API_F_WAF_URL/health" | jq .
curl -s "$API_F_WAF_URL/health?filter=1%27%20or%201%3D1%20--" -o /dev/null -w "%{http_code}\n"
```

Esperado:

- `200` en `GET /health`
- `403` en la prueba de WAF

## Paso 7: Menus de AWS que debes revisar

Usa estas rutas de consola. El nombre exacto suele verse en ingles; a la derecha dejo la referencia en espanol.

| AWS Console (EN) | Referencia ES | Que validar |
|---|---|---|
| `CloudFormation > Stacks` | `CloudFormation > Pilas` | stacks `caso-f-security-cognito` y `caso-f-security-cognito-visualization` |
| `Lambda > Functions` | `Lambda > Funciones` | funcion principal del DEMO y funcion del stack WAF |
| `Amazon Cognito > User pools` | `Amazon Cognito > Pools de usuarios` | user pool del DEMO |
| `API Gateway > APIs` | `API Gateway > API` | HTTP API del DEMO y REST API del stack WAF |
| `AWS WAF & Shield > Web ACLs` | `AWS WAF y Shield > Web ACLs` | asociacion del WebACL al REST API auxiliar |

## Paso 8: Cerrar la ventana WAF

Cuando ya tengas la evidencia, destruye el stack auxiliar:

```bash
cd caso-f-security-cognito/backend
sam delete --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --no-prompts
```

Deja el `DEMO` vivo.
