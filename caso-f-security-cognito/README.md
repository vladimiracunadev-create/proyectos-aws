# Caso F: Security First - Cognito + JWT + WAF

[![Nivel-5](https://img.shields.io/badge/Nivel-5_Seguridad-red?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-brightgreen?style=for-the-badge)]()
[![SAM](https://img.shields.io/badge/IaC-AWS_SAM-orange?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Runtime-Python_3.12-blue?style=for-the-badge)]()

La seguridad no es un parche, es la base. Este caso ensena seguridad por capas con un mensaje simple para novatos:

- el `DEMO` responde "quien eres"
- la pagina WAF responde "que ni siquiera deberia entrar"

Ambas piezas cuentan la misma historia de producto. No son dos productos distintos.

## Estado real y criterio de costo

- `DEMO principal`: [https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/](https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/)
- `WAF asociado`: [https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod](https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod)
- `Reporte de Visualizacion y Resultados`: [VISUALIZATION.md](VISUALIZATION.md)

La regla de costo del modulo es esta:

- el `DEMO` puede quedar publicado porque su costo base es practicamente cero para este laboratorio
- el `WAF` no conviene dejarlo activo por tiempo indefinido porque agrega un costo fijo cercano a `~$7/mes`
- por eso el reporte de visualizacion no se elimina: sirve como evidencia y respaldo cuando la capa WAF se destruye

La navegacion correcta del caso debe mostrar siempre:

1. `DEMO`
2. `WAF asociado`
3. `VISUALIZATION.md` como respaldo FinOps

## Explicacion sin jerga

Si una aplicacion tiene usuarios, necesita una puerta segura.

Eso es exactamente lo que hace este caso:

1. creas un usuario real
2. haces login
3. AWS emite una credencial digital
4. esa credencial abre un endpoint privado
5. luego WAF demuestra que ademas puedes bloquear trafico sospechoso antes de llegar a la app

En una frase: este caso ensena como una app deja entrar solo a usuarios validos y como agrega una segunda capa para frenar solicitudes maliciosas.

## Idea principal

El Caso F se entiende mejor asi:

1. en el `DEMO` creas un usuario real en Cognito
2. haces login y obtienes un `idToken`
3. abres `/profile` y pruebas identidad + autorizacion nativa
4. luego abres la pagina WAF y usas ese mismo token
5. ahi compruebas que la identidad sigue siendo valida, pero ahora entra una segunda capa: `REST API + Cognito Authorizer + WAF`

La relacion correcta es:

- mismo usuario
- mismo `User Pool`
- mismo token
- distinta puerta de entrada

## Enfoque

**Seguridad Perimetral.** Demo barata con `HTTP API + JWT Authorizer`, y evidencia real de perimetro con `REST API + Cognito Authorizer + WAF`.

## Que problema real resuelve

En la vida real, este patron evita cosas como:

- exponer datos privados a cualquiera que conozca la URL
- validar tokens JWT "a mano" dentro de Lambda
- mezclar autenticacion con logica de negocio
- dejar que trafico sospechoso llegue sin filtro hasta la aplicacion

## Donde se usa en la vida real

Este mismo patron aparece en:

- portales de clientes
- dashboards internos
- backoffice de operaciones
- apps moviles con login
- APIs privadas con datos de usuario

## Que demuestra cada pieza

| Pieza | Que demuestra | Costo |
|---|---|---|
| `DEMO` | Identidad real, login real, token real y acceso protegido a `/profile` | `$0` |
| Pagina WAF | La misma identidad pasando por otra puerta de entrada y un bloqueo real `403` antes de Lambda | `~$7/mes` mientras exista |
| `VISUALIZATION.md` | Ventana de evidencia, capturas, menus AWS y cierre FinOps | `$0` |

## Arquitectura mental para novatos

```text
DEMO principal
Usuario -> HTTP API -> JWT Authorizer -> Lambda
              ^            ^
              |            |
           Cognito ---- emite token

Pagina WAF auxiliar
Mismo usuario + mismo token -> WAF -> REST API -> Cognito Authorizer -> Lambda
```

## Que estas viendo en el DEMO

La landing principal del `DEMO` debe dejar claro:

- que estamos haciendo: proteger un flujo real con Cognito
- para que sirve: mover la validacion del token al borde
- que se gana: menos codigo sensible en Lambda
- que estas resolviendo: identidad y autorizacion sin criptografia manual
- que significa eso en simple: "solo entra el usuario valido"
- por que luego existe una pagina WAF: para demostrar una segunda capa distinta

## Que estas viendo en la pagina WAF

La pagina WAF no vuelve a ensenar registro y login desde cero. Su rol es conectar lo que ya probaste en el `DEMO` con la segunda capa de seguridad:

- pegas el mismo `idToken` del `DEMO`
- llamas a `/profile` para confirmar que la identidad es la misma
- ejecutas una prueba SQLi controlada
- observas un `403` antes de llegar a la logica

## Componentes

| Recurso | Rol |
|---|---|
| `UserPool` | Identidad principal del producto |
| `UserPoolClient` | Cliente sin secreto para flujo del `DEMO` |
| `SecurityFunction` | Landing, health, register, login y profile |
| `Api` en `template.yaml` | `HTTP API` con `JWT Authorizer` |
| `Api` en `template-visualization.yaml` | `REST API` con `Cognito Authorizer` |
| `WafWebAcl` | Capa perimetral para bloquear trafico sospechoso |

## Endpoints del DEMO

| Metodo | Ruta | Auth | Que muestra |
|---|---|---|---|
| `GET` | `/` | Publica | Landing principal del producto |
| `GET` | `/health` | Publica | Estado del `DEMO` |
| `POST` | `/auth/register` | Publica | Registro real en Cognito |
| `POST` | `/auth/login` | Publica | Emision de `idToken` y `accessToken` |
| `GET` | `/profile` | Requerida | Claims validados por `JWT Authorizer` |

## Endpoints de la pagina WAF

| Metodo | Ruta | Auth | Que muestra |
|---|---|---|---|
| `GET` | `/` | Publica | Landing explicativa de la segunda capa |
| `GET` | `/health` | Publica | Que el stack WAF esta vivo |
| `GET` | `/profile` | Requerida | La misma identidad del `DEMO`, pero pasando por `REST API + Cognito Authorizer + WAF` |

## Despliegue rapido

### 1. DEMO principal

```bash
cd caso-f-security-cognito/backend
sam build
sam deploy --guided
```

### 2. Recuperar outputs del DEMO

```bash
aws cloudformation describe-stacks \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --query "Stacks[0].Outputs"
```

Necesitas:

- `ApiBaseUrl`
- `UserPoolId`
- `UserPoolArn`
- `UserPoolClientId`

### 3. Pagina WAF auxiliar enlazada al DEMO

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

### 4. Enlazar el DEMO con la pagina WAF

```bash
sam deploy \
  --stack-name caso-f-security-cognito \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SupportPageUrl=https://<waf-url>
```

## Validacion rapida

### DEMO

```bash
export API_F_URL=https://<demo-url>

curl -s -X POST "$API_F_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq .

TOKEN=$(curl -s -X POST "$API_F_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq -r '.idToken')

curl -s "$API_F_URL/profile" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Pagina WAF

```bash
export API_F_WAF_URL=https://<waf-url>

curl -s "$API_F_WAF_URL/health" | jq .
curl -s "$API_F_WAF_URL/profile" -H "Authorization: Bearer $TOKEN" | jq .
curl -s "$API_F_WAF_URL/health?filter=1%27%20or%201%3D1%20--" -o /dev/null -w "%{http_code}\n"
```

Esperado:

- `200` en `/health`
- `200` en `/profile` con el mismo token del `DEMO`
- `403` en la prueba SQLi controlada

## Decision tecnica

**Por que no existe una sola URL con todo junto?**  
Porque AWS soporta bien `JWT Authorizer` nativo en `HTTP API`, pero AWS WAF se asocia a `REST API`. La forma mas didactica de ensenarlo es:

- `DEMO` barato y claro para identidad
- pagina WAF enlazada para la segunda capa

## Documentos clave

- [Paso a paso AWS](AWS_PASO_A_PASO.md)
- [Arquitectura](docs/architecture.md)
- [VISUALIZATION.md](VISUALIZATION.md)
