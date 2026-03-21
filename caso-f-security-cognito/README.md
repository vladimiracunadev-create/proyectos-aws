# Caso F: Security First - Cognito + JWT Authorizer + WAF

[![Nivel-5](https://img.shields.io/badge/Nivel-5_Seguridad-red?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-brightgreen?style=for-the-badge)]()
[![SAM](https://img.shields.io/badge/IaC-AWS_SAM-orange?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Runtime-Python_3.12-blue?style=for-the-badge)]()

La seguridad no es un parche, es la base. En este caso el producto principal vive en un `DEMO` con Cognito + HTTP API + JWT Authorizer. Cuando necesitas mostrar la capa perimetral con WAF, el DEMO enlaza a una pagina auxiliar separada que existe solo para explicar y validar ese perimetro.

## Regla simple

| Concepto | Significado real | Costo |
|---|---|---|
| `DEMO` | Producto principal, flujo completo y URL viva | `$0` |
| Pagina WAF auxiliar | Despliegue complementario enlazado desde el DEMO | `~$7/mes` mientras exista |
| `VISUALIZATION.md` | Documento de costo, ventana de uso y destruccion segura | `$0` |

## Enfoque

**Seguridad Perimetral.** Demo barata con `HTTP API + JWT Authorizer`, y evidencia real de perimetro con `REST API + Cognito Authorizer + WAF`.

## Que demuestra el DEMO

- registro y login reales con Amazon Cognito
- validacion nativa del JWT en API Gateway
- acceso a `/profile` sin criptografia manual en Lambda
- una pagina clara que explica que estas viendo, para que sirve y que problema resuelve

## Que demuestra la pagina WAF

- por que WAF vive en un despliegue aparte
- que se gana al frenar trafico malicioso antes de la aplicacion
- una prueba controlada que termina en `403`
- evidencia clara para reclutadores, revisores o capturas tecnicas

## Arquitectura

```text
Producto principal (DEMO)
Internet -> API Gateway HTTP API -> JWT Authorizer -> Lambda
                  ^                     ^
                  |                     |
               Cognito ------------- emite tokens

Pagina WAF auxiliar
Internet -> WAF -> API Gateway REST API -> Lambda
```

Ver [docs/architecture.md](docs/architecture.md) para el detalle completo.

## Endpoints del DEMO

| Metodo | Ruta | Auth | Descripcion |
|---|---|---|---|
| `GET` | `/` | Publica | Landing principal del producto |
| `GET` | `/health` | Publica | Estado del DEMO |
| `POST` | `/auth/register` | Publica | Registro en Cognito |
| `POST` | `/auth/login` | Publica | Emision de tokens |
| `GET` | `/profile` | Requerida | Perfil protegido por JWT Authorizer |

## Endpoints de la pagina WAF

| Metodo | Ruta | Auth | Descripcion |
|---|---|---|---|
| `GET` | `/` | Publica | Pagina explicativa del despliegue WAF |
| `GET` | `/health` | Publica | Health del stack auxiliar |

## Despliegue rapido

```bash
cd caso-f-security-cognito/backend

# DEMO principal
sam build
sam deploy --guided

# Pagina WAF auxiliar
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization \
  --parameter-overrides DemoPageUrl=https://<demo-url>
```

Para que el DEMO enlace a la pagina WAF, despliega o actualiza el DEMO con:

```bash
sam deploy \
  --stack-name caso-f-security-cognito \
  --parameter-overrides SupportPageUrl=https://<waf-url>
```

## Validacion rapida del DEMO

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

## Validacion rapida de la pagina WAF

```bash
export API_F_WAF_URL=https://<waf-url>

curl -s "$API_F_WAF_URL/health" | jq .
curl -s "$API_F_WAF_URL/health?filter=1%27%20or%201%3D1%20--" -o /dev/null -w "%{http_code}\n"
```

Esperado:

- `200` en `GET /health`
- `403` en la prueba SQLi controlada

## Decision tecnica

**Por que no se unifica todo en una sola URL?**  
Porque `HTTP API + JWT Authorizer` es el mejor camino para el DEMO barato, pero AWS WAF se asocia a `REST API`. El producto se mantiene claro dejando el DEMO como principal y WAF como pagina auxiliar enlazada.

## Documentos clave

- [Paso a paso AWS](AWS_PASO_A_PASO.md)
- [Arquitectura](docs/architecture.md)
- [VISUALIZATION.md](VISUALIZATION.md)
