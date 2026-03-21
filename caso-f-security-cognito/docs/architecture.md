# Arquitectura: Caso F - Security First

> Stack compartido: Cognito + Lambda + API Gateway  
> Modalidades: DEMO (HTTP API) y VISUALIZATION (REST API + WAF)

## Decision principal

El Caso F usa **dos arquitecturas hermanas** porque hay una restriccion real de AWS:

- `HTTP API` soporta JWT Authorizer nativo y es la mejor opcion para demo barata.
- `AWS WAF` se asocia a `REST API`, no a `HTTP API`.

La solucion final no intenta forzar una combinacion imposible. En vez de eso, separa el caso en:

1. `DEMO`: despliegue vivo, costo base cero, HTTP API + JWT Authorizer.
2. `VISUALIZATION`: despliegue temporal, evidencia y capturas, REST API + Cognito Authorizer + WAF.

## Diagrama 1: Decision de arquitectura

```mermaid
flowchart TD
    Goal["Objetivo del caso F"]
    Goal --> Cheap["Demo barata y permanente"]
    Goal --> Perimeter["Evidencia real de perimetro con WAF"]

    Cheap --> Demo["template.yaml<br/>HTTP API<br/>JWT Authorizer"]
    Perimeter --> Viz["template-visualization.yaml<br/>REST API<br/>Cognito Authorizer + WAF"]
```

## Diagrama 2: Modalidad DEMO

```mermaid
sequenceDiagram
    actor U as Usuario
    participant APIGW as API Gateway HTTP API
    participant L as Lambda
    participant C as Cognito

    U->>APIGW: POST /auth/register
    APIGW->>L: invoke
    L->>C: sign_up
    C-->>L: user created
    L-->>U: 201

    U->>APIGW: POST /auth/login
    APIGW->>L: invoke
    L->>C: initiate_auth
    C-->>L: accessToken + idToken
    L-->>U: 200

    U->>APIGW: GET /profile + Bearer idToken
    APIGW->>APIGW: JWT Authorizer valida firma, issuer y audience
    APIGW->>L: invoke con claims
    L-->>U: 200 profile
```

## Diagrama 3: Modalidad VISUALIZATION

```mermaid
sequenceDiagram
    actor U as Usuario
    participant W as AWS WAF
    participant APIGW as API Gateway REST API
    participant L as Lambda
    participant C as Cognito

    U->>W: Request
    alt Payload malicioso
        W-->>U: 403 bloqueado
    else Request valido
        W->>APIGW: Forward
        APIGW->>APIGW: Cognito Authorizer valida token
        APIGW->>L: invoke con claims
        L-->>U: 200 profile
    end
```

## Diagrama 4: Componentes compartidos

```mermaid
flowchart LR
    subgraph Shared["Recursos compartidos"]
        UP["Cognito User Pool"]
        UC["User Pool Client"]
        L["SecurityFunction"]
        PRE["PreSignUpFunction"]
    end

    subgraph Demo["Modo DEMO"]
        H["HTTP API"]
        J["JWT Authorizer"]
    end

    subgraph Viz["Modo VISUALIZATION"]
        R["REST API"]
        A["Cognito Authorizer"]
        W["WAF WebACL"]
    end

    UP --> UC
    UP --> PRE
    H --> J
    J --> L
    R --> A
    A --> L
    W --> R
    L <--> UP
```

## Beneficios del diseno

- No hay codigo de validacion criptografica dentro de Lambda.
- La demo sigue viva sin costo base.
- WAF se prueba de forma autentica cuando se necesita evidencia.
- El frontend funciona en ambos modos porque resuelve automaticamente la base path.
- El mismo handler soporta eventos de HTTP API v2 y REST API v1.

## Riesgos controlados

| Riesgo | Mitigacion |
|---|---|
| Mezclar WAF con HTTP API | Separamos templates |
| Mostrar claims incompletos | `/profile` usa `idToken` |
| Romper la landing en REST API por el stage `/Prod` | El frontend calcula la base URL en runtime |
| Mantener costo fijo por WAF | `VISUALIZATION.md` documenta deploy -> capture -> destroy |

## Referencias

- [README del Caso F](../README.md)
- [Paso a paso AWS](../AWS_PASO_A_PASO.md)
- [Reporte de visualization](../VISUALIZATION.md)
- [Template DEMO](../backend/template.yaml)
- [Template VISUALIZATION](../backend/template-visualization.yaml)
