# Reporte de Visualization y Resultados - Caso F

## Por que existe este documento

El Caso F ahora tiene dos modalidades:

- `DEMO`: queda bien como demo viva porque no tiene costo base.
- `VISUALIZATION`: existe para demostrar WAF real y debe destruirse al terminar.

Este reporte es la guia para capturar la evidencia de la modalidad `VISUALIZATION` sin confundirla con la demo barata.

## Regla de evidencia

La evidencia del Caso F se divide asi:

- `DEMO` valida que el producto existe y funciona de verdad.
- `DEMO` tambien puede aportar las capturas funcionales de registro, login y perfil.
- `VISUALIZATION` aporta las capturas especificas que exigen REST API + WAF: asociacion del WebACL y bloqueo de trafico malicioso.

## Resumen de la estrategia

| Modalidad | Vive publicada | Costo base | Evidencia principal |
|---|---|---|---|
| `DEMO` | Si | $0 | URL en vivo |
| `VISUALIZATION` | No, solo ventanas controladas | ~`$7/mes` | Este documento + capturas |

## Stack a desplegar para evidencia

```bash
cd caso-f-security-cognito/backend
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM
```

Outputs a guardar:

- `ApiBaseUrl`
- `UserPoolId`
- `UserPoolClientId`
- `FunctionName`
- `WebAclArn`
- `DeploymentMode`

## Checklist de evidencia

### 1. CloudFormation

Captura donde se vea:

- stack `caso-f-security-cognito-visualization`
- estado `CREATE_COMPLETE` o `UPDATE_COMPLETE`
- region correcta
- output `ApiBaseUrl`

### 2. API Gateway REST API

Captura donde se vea:

- stage `Prod`
- rutas `GET /`, `GET /health`, `POST /auth/register`, `POST /auth/login`, `GET /profile`
- authorizer de Cognito activo en `/profile`

### 3. Cognito

Captura donde se vea:

- User Pool creado
- App Client sin secreto
- password policy

### 4. WAF

Captura donde se vea:

- WebACL asociado al REST API
- `AWSManagedRulesCommonRuleSet`
- `AWSManagedRulesSQLiRuleSet`

### 5. Landing inicial

Puede salir desde `DEMO` o `VISUALIZATION`. Si la pantalla es puramente funcional y no depende de WAF, se acepta capturarla desde `DEMO`.

Captura de `GET /` mostrando:

- hero del Caso F
- explicacion de los dos modos
- panel de demo de 3 pasos

### 6. Registro exitoso

Preferencia: capturar desde `DEMO`, porque es la prueba viva del producto funcionando.

Captura con:

- respuesta `201`
- usuario creado
- paso 1 completado

### 7. Login exitoso

Preferencia: capturar desde `DEMO`, usando el flujo real de login.

Captura con:

- `idToken` visible parcialmente
- paso 2 completado
- respuesta `200`

### 8. Perfil protegido

Preferencia: capturar desde `DEMO`, porque demuestra authorizer nativo activo y producto real en ejecucion.

Captura con:

- llamada a `/profile`
- `email`, `sub` y `name`
- badge de exito

### 9. WAF bloqueando SQLi

Esta captura si debe salir de `VISUALIZATION`.

Ejecuta:

```bash
curl -s "$API_F_URL/auth/login?q=1' OR '1'='1" -w "\nHTTP: %{http_code}\n"
```

Captura donde se vea:

- `HTTP 403`
- request bloqueado por WAF

### 10. Limpieza

Captura o evidencia de:

```bash
sam delete --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --region us-east-2
```

## Nombres sugeridos para capturas

Guarda las imagenes en `caso-f-security-cognito/img/` con nombres como:

- `cloudformation-stack-complete.png`
- `rest-api-routes.png`
- `cognito-user-pool.png`
- `waf-web-acl.png`
- `landing-initial.png`
- `register-success.png`
- `login-success.png`
- `profile-success.png`
- `waf-sqli-blocked.png`

## Verificacion final

| Hito | Estado esperado |
|---|---|
| Stack visualization desplegado | OK |
| REST API con authorizer | OK |
| WAF asociado | OK |
| Login entrega `idToken` | OK |
| `/profile` devuelve claims | OK |
| SQLi de prueba devuelve `403` | OK |
| Stack destruido al terminar | CRITICO |

## Cierre FinOps

La evidencia de WAF vale mas que dejar el recurso encendido permanentemente.  
La regla para este caso es simple:

1. desplegar
2. validar
3. capturar
4. destruir
