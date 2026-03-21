# Caso F: Security First - Cognito + Authorizer nativo + WAF

[![Nivel-5](https://img.shields.io/badge/Nivel-5_Seguridad-red?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-brightgreen?style=for-the-badge)]()
[![SAM](https://img.shields.io/badge/IaC-AWS_SAM-orange?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Runtime-Python_3.12-blue?style=for-the-badge)]()

La seguridad no es un parche, es la base. Este caso demuestra identidad gestionada con Cognito, validacion nativa del token en API Gateway y una modalidad separada con WAF para capturar evidencia real del perimetro sin dejar costo fijo activo fuera del laboratorio.

## Punto clave

AWS WAF no se asocia a API Gateway HTTP API. Por eso el Caso F se implementa en **dos modalidades validas**:

| Modalidad | Template | API Gateway | Authorizer | WAF | Uso recomendado |
|---|---|---|---|---|---|
| `DEMO` | `backend/template.yaml` | HTTP API | JWT Authorizer nativo | No | Demo permanente, costo base cero |
| `VISUALIZATION` | `backend/template-visualization.yaml` | REST API | Cognito User Pool Authorizer | Si | Capturas, evidencia y validacion perimetral |

La regla del caso es esta: **DEMO prueba que el producto existe y funciona de verdad**. Luego, esa misma experiencia funcional sirve para las capturas de producto, y `VISUALIZATION` agrega las evidencias especificas del perimetro con WAF.

## Objetivo

- Gestionar identidades de usuario con Amazon Cognito.
- Proteger `/profile` sin escribir criptografia en Lambda.
- Mantener una demo barata y, a la vez, una variante seria para mostrar WAF real.

## Arquitectura

```text
Modo DEMO
Internet -> API Gateway HTTP API -> JWT Authorizer -> Lambda
                  ^                     ^
                  |                     |
               Cognito ------------- emite tokens

Modo VISUALIZATION
Internet -> WAF -> API Gateway REST API -> Cognito Authorizer -> Lambda
                 ^                           ^
                 |                           |
              reglas managed ----------- Cognito
```

Ver [docs/architecture.md](docs/architecture.md) para el diagrama completo y la decision tecnica.

## Componentes

| Recurso | Modalidad | Descripcion |
|---|---|---|
| `UserPool` | Ambas | Email como username, auto-verified, password policy |
| `UserPoolClient` | Ambas | `USER_PASSWORD_AUTH`, sin client secret |
| `SecurityFunction` | Ambas | Registro, login, profile, health |
| `PreSignUpFunction` | Ambas | Auto-confirma usuarios para demo controlada |
| `Api` | `DEMO` | `AWS::Serverless::HttpApi` con JWT Authorizer |
| `Api` | `VISUALIZATION` | `AWS::Serverless::Api` con Cognito Authorizer |
| `WafWebAcl` | `VISUALIZATION` | Common Rules + SQLi Rules para validar perimetro |

## Endpoints

| Metodo | Ruta | Auth | Descripcion |
|---|---|---|---|
| `GET` | `/` | Publica | Landing interactiva |
| `GET` | `/health` | Publica | Estado del servicio y modalidad desplegada |
| `POST` | `/auth/register` | Publica | Crea usuario en Cognito |
| `POST` | `/auth/login` | Publica | Devuelve `accessToken`, `idToken`, `refreshToken` |
| `GET` | `/profile` | Requerida | Devuelve claims ya validados por API Gateway |

## Despliegue rapido

```bash
cd caso-f-security-cognito/backend

# Modalidad DEMO
sam build
sam deploy --guided

# Modalidad VISUALIZATION
sam build --template-file template-visualization.yaml
sam deploy --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization
```

## Validacion rapida

```bash
# Tests unitarios
python -m pytest caso-f-security-cognito/backend/tests/ -v --tb=short

# Smoke test demo o visualization
export API_F_URL=https://<api-id>.execute-api.us-east-2.amazonaws.com
bash scripts/smoke/smoke_caso_f.sh

# Smoke con chequeo WAF
EXPECT_WAF=true bash scripts/smoke/smoke_caso_f.sh
```

En `/profile`, usa preferentemente el `idToken`:

```bash
TOKEN=$(curl -s -X POST "$API_F_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@demo.com","password":"Demo1234"}' | jq -r '.idToken')

curl -s "$API_F_URL/profile" -H "Authorization: Bearer $TOKEN" | jq .
```

## Limpieza

```bash
# Demo
sam delete --stack-name caso-f-security-cognito

# Visualization
sam delete --template-file template-visualization.yaml \
  --stack-name caso-f-security-cognito-visualization
```

## Decisiones tecnicas

**Por que dos templates en vez de un flag `DeployWAF`?**  
Porque HTTP API + JWT Authorizer es el camino correcto para la demo barata, pero WAF se asocia a REST API. Separar los templates evita prometer una combinacion que AWS no soporta.

**Por que usar `idToken` en `/profile`?**  
Porque contiene claims de identidad como `email` y `name`, que son los que el endpoint muestra al reclutador o al evaluador del laboratorio.

**Por que mantener `USER_PASSWORD_AUTH`?**  
Porque simplifica `curl`, smoke tests y la landing interactiva. En produccion, `SRP_AUTH` o flujos hosted UI son preferibles.

## Relacion con otros casos

- **Caso E**: agrega identidad sobre la API serverless con datos.
- **Caso H**: la siguiente mejora natural es observabilidad de rechazos, login failures y WAF.
- **Caso I**: prerequisito directo antes de exponer endpoints de IA.

## Links

- [Roadmap Principal](../README.md)
- [Arquitectura detallada](docs/architecture.md)
- [Paso a paso AWS](AWS_PASO_A_PASO.md)
- [Reporte de visualization](VISUALIZATION.md)
