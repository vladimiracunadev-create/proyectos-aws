# 🔐 Arquitectura: Caso F — Security First (Cognito + JWT + WAF)

> **Stack**: AWS Cognito + API Gateway JWT Authorizer + WAF opcional + AWS SAM
> **Nivel**: 5 — Seguridad Perimetral e Identidad

---

## Visión general

Este caso implementa el principio **"seguridad como infraestructura"**: ninguna capa de
defensa vive en el código de la Lambda, todo está declarado en el SAM template y gestionado
por servicios administrados de AWS.

El modelo se organiza en cuatro capas independientes:

1. **WAF** filtra tráfico malicioso antes de que llegue al API (opcional, ~$5/mes)
2. **API Gateway** valida el token JWT criptográficamente sin ejecutar código propio
3. **Cognito** gestiona identidades: registro, login y emisión de tokens RS256
4. **Lambda** solo lee claims ya validados — nunca toca ni verifica el token

El resultado es una superficie de ataque mínima: si el token es inválido, la Lambda
nunca se invoca. Si el tráfico es malicioso, WAF lo absorbe antes del API.

---

## 📐 Diagrama 1: Flujo completo de autenticación (registro → login → perfil)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant APIGW as API Gateway<br/>HTTP API
    participant LM as Lambda<br/>SecurityFunction
    participant COG as Cognito<br/>User Pool
    participant PRE as Lambda<br/>PreSignUpFunction

    Note over U,PRE: Paso 1 — Registro
    U->>APIGW: POST /auth/register {email, password}
    APIGW->>LM: invoke (ruta pública — sin JWT)
    LM->>COG: sign_up(ClientId, Username, Password)
    COG->>PRE: trigger PreSignUp event
    PRE-->>COG: autoConfirmUser=True, autoVerifyEmail=True
    COG-->>LM: {UserSub: "abc-123", UserConfirmed: true}
    LM-->>APIGW: 201 {ok, userSub}
    APIGW-->>U: 201 {ok, userSub}

    Note over U,PRE: Paso 2 — Login
    U->>APIGW: POST /auth/login {email, password}
    APIGW->>LM: invoke (ruta pública — sin JWT)
    LM->>COG: initiate_auth(USER_PASSWORD_AUTH)
    COG-->>LM: {AccessToken, IdToken, RefreshToken, ExpiresIn}
    LM-->>APIGW: 200 {tokens}
    APIGW-->>U: 200 {accessToken, idToken, ...}

    Note over U,PRE: Paso 3 — Acceso protegido
    U->>APIGW: GET /profile + Authorization: <AccessToken>
    APIGW->>APIGW: JWT Authorizer valida firma RS256,<br/>issuer y audience (Cognito)
    Note right of APIGW: Si falla: 403 sin invocar Lambda
    APIGW->>LM: invoke con requestContext.authorizer.jwt.claims
    LM-->>APIGW: 200 {email, sub, name, emailVerified}
    APIGW-->>U: 200 {perfil con claims}
```

---

## 📐 Diagrama 2: Las cuatro capas de defensa

```mermaid
flowchart TD
    Internet([🌐 Internet])

    subgraph Capa1["Capa 1 — Perímetro (opcional)"]
        WAF["☁️ AWS WAF WebACL<br/>AWSManagedRulesCommonRuleSet<br/>AWSManagedRulesSQLiRuleSet<br/><br/>Bloquea: SQLi · XSS · IPs maliciosas<br/>Antes de que llegue a API Gateway"]
    end

    subgraph Capa2["Capa 2 — Autenticación de token"]
        JWTAUTH["🔑 API GW JWT Authorizer<br/>issuer: cognito-idp.{region}.amazonaws.com/{pool}<br/>audience: {clientId}<br/><br/>Valida: firma RS256 · expiración · issuer · audience<br/>Sin código Lambda · Sin cold start extra"]
    end

    subgraph Capa3["Capa 3 — Identidad"]
        UP["👤 Cognito User Pool<br/>Registro · Login · Tokens JWT RS256<br/>Pre-Signup trigger → auto-confirm (demo)"]
    end

    subgraph Capa4["Capa 4 — Lógica de negocio"]
        LM["⚡ Lambda SecurityFunction<br/>Lee claims inyectados en requestContext<br/>Nunca valida ni decodifica el token"]
    end

    Internet -->|"HTTPS"| WAF
    WAF -->|"Permitido ✓"| JWTAUTH
    WAF -->|"Bloqueado ✗ → 403"| Internet
    JWTAUTH -->|"Token válido → claims inyectados"| LM
    JWTAUTH -->|"Token inválido → 403"| Internet
    UP <-->|"sign_up / initiate_auth"| LM
    LM -->|"Rutas públicas (no pasan por JWT Authorizer)"| UP

    style WAF fill:#ff9900,color:#000,stroke:#cc7700
    style JWTAUTH fill:#c77dff,color:#000,stroke:#9b3fff
    style UP fill:#7b2ff7,color:#fff,stroke:#5a1fbe
    style LM fill:#4cc9f0,color:#000,stroke:#2a99c0
    style Capa1 fill:#fff8ee,stroke:#ff9900,stroke-width:2px
    style Capa2 fill:#f9f0ff,stroke:#c77dff,stroke-width:2px
    style Capa3 fill:#f0ebff,stroke:#7b2ff7,stroke-width:2px
    style Capa4 fill:#e8f9ff,stroke:#4cc9f0,stroke-width:2px
```

---

## 📐 Diagrama 3: Arquitectura completa AWS (SAM stack)

```mermaid
flowchart LR
    subgraph Dev["🧑‍💻 Desarrollador"]
        CODE["app.py<br/>template.yaml"]
        SAM["sam build<br/>sam deploy"]
    end

    subgraph CFN["☁️ CloudFormation Stack"]
        direction TB

        subgraph Auth["🔐 Identidad"]
            UP["AWS::Cognito::UserPool<br/>email username · password policy"]
            UC["AWS::Cognito::UserPoolClient<br/>USER_PASSWORD_AUTH · no secret"]
        end

        subgraph APIG["🌐 API Gateway HTTP API"]
            API["AWS::Serverless::HttpApi<br/>CORS + JWT Authorizer"]
        end

        subgraph Lambdas["⚡ AWS Lambda — Python 3.12"]
            LM["SecurityFunction<br/>handler: app.handler<br/>GET / · GET /health<br/>POST /auth/register · POST /auth/login<br/>GET /profile (JWT)"]
            LP["PreSignUpFunction<br/>handler: app.pre_signup_trigger<br/>autoConfirmUser (demo)"]
        end

        subgraph WAFSec["🛡️ WAF (opcional)"]
            WACL["AWS::WAFv2::WebACL<br/>DeployWAF=true"]
            WASSOC["AWS::WAFv2::WebACLAssociation"]
        end
    end

    CODE --> SAM
    SAM -->|"sam deploy"| CFN
    UP -->|"Pre-Signup trigger"| LP
    API -->|"JWT Authorizer"| UC
    UC <-->|"valida audience"| UP
    WACL --> WASSOC
    WASSOC -->|"asocia WebACL"| API
```

---

## 📐 Diagrama 4: Por qué el JWT Authorizer no necesita código Lambda

```mermaid
flowchart TD
    subgraph Sin["❌ Patrón clásico — Custom Authorizer Lambda"]
        direction TB
        REQ1["Request + token"] --> LA["Lambda Authorizer<br/>(código propio)"]
        LA --> VERIF["Verificar firma RS256<br/>Validar exp · iss · aud<br/>Decodificar claims<br/>Manejar errores cripto"]
        VERIF --> DEC["Devolver Allow/Deny policy"]
        DEC --> MAIN1["Lambda principal"]
        LA -.->|"cold start extra<br/>+ costo extra<br/>+ superficie de ataque"| MAIN1
    end

    subgraph Con["✅ Patrón Caso F — JWT Authorizer nativo API GW"]
        direction TB
        REQ2["Request + token"] --> JWTGW["API Gateway<br/>JWT Authorizer<br/>(configuración declarativa)"]
        JWTGW -->|"claims en requestContext"| MAIN2["Lambda principal<br/>solo lee claims<br/>0 código de cripto"]
        JWTGW -->|"token inválido"| BLOCK["403 — Lambda<br/>nunca se invoca"]
    end

    style Sin fill:#fff0f0,stroke:#ff6b6b,stroke-width:2px
    style Con fill:#f0fff4,stroke:#7ef0b8,stroke-width:2px
    style LA fill:#ffcccc,color:#000
    style JWTGW fill:#7ef0b8,color:#000
    style BLOCK fill:#ff9797,color:#000
```

---

## 🔧 Componentes y roles

| Componente | Servicio AWS | Función | Costo demo |
|---|---|---|---|
| **WAF WebACL** | WAFv2 | Bloquea SQLi, XSS, IPs maliciosas antes del API | ~$0.35/día (evitar en demo) |
| **JWT Authorizer** | API Gateway HTTP API | Valida firma RS256, issuer y audience — sin código | Gratis (incluido en API GW) |
| **User Pool** | Cognito | Gestiona identidades, emite tokens JWT estándar | Gratis hasta 50.000 MAU |
| **App Client** | Cognito | Credencial sin secreto para `USER_PASSWORD_AUTH` | Gratis |
| **SecurityFunction** | Lambda Python 3.12 | Registro, login, perfil, health — lee claims | Free tier cubre demos |
| **PreSignUpFunction** | Lambda Python 3.12 | Auto-confirma usuarios sin verificación de email | Free tier cubre demos |
| **SAM template** | CloudFormation | IaC declarativo — el stack nace y muere junto | Gratis |

---

## 💡 Decisiones de diseño

| Decisión | Motivo |
|---|---|
| JWT Authorizer nativo en lugar de Custom Authorizer Lambda | Elimina código de criptografía propio, cold start extra y superficie de ataque. La infraestructura valida, no el código. |
| `USER_PASSWORD_AUTH` en lugar de `SRP_AUTH` | SRP (Secure Remote Password) es más seguro pero incompatible con curl y smoke tests. En producción usar SRP; en demo, `USER_PASSWORD_AUTH` sobre HTTPS es aceptable. |
| Pre-Signup trigger con `autoConfirmUser=True` | Elimina el paso de verificación de email para facilitar la demo. Documentado explícitamente — **nunca en producción**. |
| `DeployWAF=false` por defecto | WAF tiene costo fijo de ~$5/mes independiente del tráfico. Para portafolio/demo es innecesario. Se activa con un solo parámetro SAM cuando se necesita validar el perímetro. |
| App Client sin secreto de cliente | Necesario para que `initiate_auth` funcione desde Lambda sin almacenar secretos en código. El secreto de cliente exige HMAC en cada llamada — innecesario con `USER_PASSWORD_AUTH`. |
| Claims leídos desde `requestContext` (no del token) | API Gateway inyecta los claims ya validados en el contexto. La Lambda no necesita importar ni `PyJWT` ni `cryptography`. |
| Rutas públicas con `Auth: Authorizer: NONE` | SAM aplica el JWT Authorizer por defecto a todas las rutas. Las rutas de auth y health se eximen explícitamente para que no exijan token. |

---

## 🎓 Qué aprende un reclutador de este caso

- Que separas **autenticación** (quién eres — Cognito) de **autorización** (si puedes — JWT Authorizer).
- Que usas servicios administrados de AWS para validar tokens: cero código de criptografía en Lambda.
- Que entiendes el flujo completo OAuth2/OIDC: sign_up → confirm → initiate_auth → tokens → claims.
- Que aplicas **defensa en profundidad**: WAF → API GW → Cognito → Lambda, cuatro capas independientes.
- Que declaras la seguridad como IaC (SAM/CloudFormation), no como clics manuales en la consola.
- Que conoces el costo real de WAF y decides cuándo activarlo con un parámetro SAM.
- Que este caso es el prerequisito directo del Caso I (GenAI Bedrock), donde los endpoints de IA no pueden quedar públicos.

---

## ➡️ Siguiente paso natural

El complemento inmediato de este caso es:

- **Caso I (GenAI Bedrock)**: proteger los endpoints de Bedrock con el mismo JWT Authorizer de Cognito. Sin Caso F, los endpoints de IA quedan públicos.
- **Caso H (Observability)**: añadir métricas CloudWatch de intentos de registro fallidos, logins erróneos y rechazos JWT para detectar ataques de fuerza bruta.
- **Producción**: sustituir `autoConfirmUser=True` en el trigger por un flujo real de verificación de email con SES. Cambiar `USER_PASSWORD_AUTH` a `SRP_AUTH` para que la contraseña nunca viaje en la red.

---

## 🔗 Referencias

- [README del Caso F](../README.md)
- [Guía Paso a Paso AWS](../AWS_PASO_A_PASO.md)
- [SAM template](../backend/template.yaml)
- [Handler Lambda](../backend/src/app.py)
