# Arquitectura — Caso F: Security First

## Diagrama de flujo

```mermaid
flowchart TD
    subgraph Client["Cliente (Browser / App)"]
        U[Usuario]
    end

    subgraph WAF["AWS WAF (opcional)"]
        W[WebACL<br/>AWSManagedRulesCommonRuleSet<br/>AWSManagedRulesSQLiRuleSet]
    end

    subgraph APIGW["API Gateway (HTTP API)"]
        PUB[Rutas públicas<br/>POST /auth/register<br/>POST /auth/login<br/>GET /health<br/>GET /]
        JWT[JWT Authorizer<br/>Cognito issuer + audience]
        PROT[Ruta protegida<br/>GET /profile]
    end

    subgraph Cognito["Amazon Cognito"]
        UP[User Pool<br/>Email username<br/>Password policy]
        UC[App Client<br/>USER_PASSWORD_AUTH<br/>Sin secreto]
        TRG[Pre-Signup Trigger<br/>autoConfirmUser]
    end

    subgraph Lambda["AWS Lambda — Python 3.12"]
        LM[SecurityFunction<br/>app.handler]
        LP[PreSignUpFunction<br/>app.pre_signup_trigger]
    end

    U -->|"1. Tráfico HTTPS"| W
    W -->|"2. Permitir / Bloquear"| APIGW
    PUB -->|"POST /auth/register"| LM
    PUB -->|"POST /auth/login"| LM
    LM -->|"sign_up()"| UP
    UP -->|"Pre-Signup event"| LP
    LP -->|"autoConfirmUser=True"| UP
    LM -->|"initiate_auth()"| UC
    UC -->|"AccessToken + IdToken"| LM
    U -->|"3. GET /profile + Authorization: <token>"| JWT
    JWT -->|"Valida issuer/audience/firma"| PROT
    PROT -->|"requestContext.authorizer.jwt.claims"| LM
    LM -->|"200 + claims"| U

    style W fill:#ff9900,color:#000
    style JWT fill:#c77dff,color:#000
    style UP fill:#7b2ff7,color:#fff
    style LM fill:#4cc9f0,color:#000
```

## Capas de seguridad

| Capa | Componente | Responsabilidad |
|------|-----------|-----------------|
| 1 — Perimetro | WAF WebACL | Bloquea SQLi, XSS, IPs maliciosas antes del API |
| 2 — Autenticacion | Cognito User Pool | Gestiona identidades, emite JWT estándar (RS256) |
| 3 — Autorizacion | API GW JWT Authorizer | Valida firma, issuer y audience sin código Lambda |
| 4 — Lógica | Lambda SecurityFunction | Lee claims inyectados, nunca valida el token |

## Flujo de registro y login

```
Cliente          API Gateway         Lambda           Cognito
   |                  |                 |                 |
   |-- POST /register -->               |                 |
   |                  |-- invoke ------>|                 |
   |                  |                 |-- sign_up() -->|
   |                  |                 |                 |-- PreSignUp trigger -->
   |                  |                 |                 |<-- autoConfirmUser=True --
   |                  |                 |<-- UserSub ----|
   |<-- 201 {ok,sub} -|                 |                 |
   |                  |                 |                 |
   |-- POST /login -->|                 |                 |
   |                  |-- invoke ------>|                 |
   |                  |                 |-- initiate_auth() -->
   |                  |                 |<-- AccessToken + IdToken + RefreshToken --
   |<-- 200 {tokens} -|                 |                 |
   |                  |                 |                 |
   |-- GET /profile + Bearer token -->  |                 |
   |                  |-- validate JWT (issuer + audience + firma RS256)
   |                  |-- inject claims into requestContext
   |                  |-- invoke ------>|                 |
   |                  |                 |-- read claims --|
   |<-- 200 {email, sub} --------------|                 |
```

## Notas de coste

- **Cognito**: gratuito hasta 50 000 MAU (Monthly Active Users).
- **WAF**: ~$5 USD/mes base + $1 por millón de requests. Por eso `DeployWAF=false` por defecto en demos.
- **Lambda + API GW**: capa gratuita cubre demos sin costo.
