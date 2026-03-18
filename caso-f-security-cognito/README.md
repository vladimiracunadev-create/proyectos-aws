# Caso F: Security First — Cognito + JWT + WAF

[![Nivel-5](https://img.shields.io/badge/Nivel-5_Seguridad-red?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Completado-brightgreen?style=for-the-badge)]()
[![SAM](https://img.shields.io/badge/IaC-AWS_SAM-orange?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Runtime-Python_3.12-blue?style=for-the-badge)]()

La seguridad no es un parche, es la base. Este caso implementa el modelo de seguridad perimetral en AWS: identidades gestionadas por Cognito, tokens JWT validados nativamente por API Gateway y WAF opcional como primera línea de defensa.

---

## Objetivo

Implementar el **modelo de responsabilidad compartida** de AWS aplicado a una API serverless:

- Gestionar identidades de usuario con **Amazon Cognito** (registro, login, tokens JWT RS256)
- Proteger endpoints con el **JWT Authorizer nativo** de API Gateway HTTP API (sin código de criptografía en Lambda)
- Añadir una capa de perimetro con **AWS WAF** (optional, desactivado por defecto en demos)

## Arquitectura

```
Internet → [WAF opcional] → [API Gateway HTTP API] → [Lambda Python]
                                      ↑                      ↑
                              JWT Authorizer          handle_register
                              (valida token)          handle_login
                                      ↑               handle_profile
                              Cognito User Pool       handle_health
                              (emite tokens)
```

Ver [docs/architecture.md](docs/architecture.md) para el diagrama completo.

## Componentes

| Recurso | Tipo | Descripción |
|---------|------|-------------|
| `UserPool` | `AWS::Cognito::UserPool` | Email como username, Pre-Signup trigger para auto-confirm en demo |
| `UserPoolClient` | `AWS::Cognito::UserPoolClient` | `USER_PASSWORD_AUTH`, sin secreto de cliente |
| `Api` | `AWS::Serverless::HttpApi` | CORS + JWT Authorizer de Cognito |
| `SecurityFunction` | `AWS::Serverless::Function` | Handler principal — Python 3.12 |
| `PreSignUpFunction` | `AWS::Serverless::Function` | Trigger Cognito — auto-confirma usuarios en demo |
| `WafWebAcl` | `AWS::WAFv2::WebACL` | SQLi + Common Rules (solo si `DeployWAF=true`) |

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `GET` | `/` | Pública | Landing page interactiva |
| `GET` | `/health` | Pública | Estado del servicio |
| `POST` | `/auth/register` | Pública | Crea usuario en Cognito User Pool |
| `POST` | `/auth/login` | Pública | Devuelve AccessToken + IdToken + RefreshToken |
| `GET` | `/profile` | **JWT requerido** | Devuelve claims del token validado |

## Despliegue rápido

```bash
cd caso-f-security-cognito/backend

# Sin WAF (demo, sin costo base)
sam build && sam deploy --guided

# Con WAF (~$5 USD/mes base)
sam deploy --parameter-overrides DeployWAF=true
```

## Tests

```bash
# Unitarios
pytest backend/tests/ -v --tb=short

# Smoke test (requiere API_F_URL)
export API_F_URL=https://<api-id>.execute-api.us-east-2.amazonaws.com
bash ../../scripts/smoke/smoke_caso_f.sh
```

## Limpieza

```bash
sam delete --stack-name caso-f-security-cognito
```

> **Importante**: Si desplegaste con `DeployWAF=true`, el `sam delete` también elimina el WebACL y detiene el cobro de ~$5/mes.

## Decisiones técnicas

**¿Por qué JWT Authorizer en lugar de Custom Authorizer Lambda?**
El JWT Authorizer nativo de API Gateway HTTP API verifica la firma RS256, el issuer y el audience de Cognito sin ejecutar ninguna Lambda. Es más barato, más rápido (sin cold start extra) y elimina una clase entera de bugs de implementación.

**¿Por qué `USER_PASSWORD_AUTH` y no `SRP_AUTH`?**
Para una demo con curl y scripts de smoke test es necesario enviar email+password en texto plano sobre HTTPS. En producción, `SRP_AUTH` (Secure Remote Password) es preferible porque la contraseña nunca viaja por la red, ni siquiera cifrada.

**¿Por qué WAF opcional con `DeployWAF=false` por defecto?**
WAF tiene un costo fijo de ~$5 USD/mes independiente del tráfico. Para portafolio/demo es un gasto innecesario. El parámetro SAM permite activarlo con un solo flag cuando se necesite validar el perimetro.

## Relación con otros casos

- **Caso E** (DynamoDB): Caso F añade la capa de identidad necesaria antes de persistir datos de usuario.
- **Caso G** (Event-Driven): Los eventos de registro/login pueden publicarse a SNS/EventBridge como extensión.
- **Caso I** (IA Generativa): Los endpoints de Bedrock **requieren** autenticación. Caso F es prerequisito directo.

## Links

- ⬅️ [Roadmap Principal](../README.md)
- 🏗️ [Arquitectura detallada](docs/architecture.md)
- 📋 [Paso a paso AWS](AWS_PASO_A_PASO.md)
