# Arquitectura: Caso F - identidad primero, perimetro despues

## Idea central

El Caso F tiene una sola historia tecnica:

- primero demuestras identidad
- despues demuestras perimetro

Eso se reparte en dos despliegues porque AWS no permite exactamente la misma combinacion en una sola puerta de entrada:

- `HTTP API` soporta muy bien `JWT Authorizer`
- `AWS WAF` se asocia a `REST API`

## Regla de lectura

| Pieza | Pregunta que responde |
|---|---|
| `DEMO` | `quien eres` |
| Pagina WAF | `que trafico ni siquiera deberia entrar` |

## Diagrama 1: producto completo

```mermaid
flowchart TD
    U["Usuario"]
    D["DEMO principal<br/>HTTP API + JWT Authorizer"]
    W["Pagina WAF auxiliar<br/>REST API + Cognito Authorizer + WAF"]
    C["Cognito User Pool compartido"]
    L["Lambda"]

    U --> D
    U --> W
    C --> D
    C --> W
    D --> L
    W --> L
```

## Diagrama 2: lo que prueba el DEMO

```mermaid
sequenceDiagram
    actor U as Usuario
    participant APIGW as HTTP API
    participant C as Cognito
    participant L as Lambda

    U->>APIGW: POST /auth/register
    APIGW->>L: invoke
    L->>C: sign_up
    C-->>L: usuario creado
    L-->>U: 201

    U->>APIGW: POST /auth/login
    APIGW->>L: invoke
    L->>C: initiate_auth
    C-->>L: idToken
    L-->>U: 200

    U->>APIGW: GET /profile + Bearer idToken
    APIGW->>APIGW: JWT Authorizer valida token
    APIGW->>L: invoke con claims
    L-->>U: 200
```

## Diagrama 3: lo que prueba la pagina WAF

```mermaid
sequenceDiagram
    actor U as Usuario
    participant WAF as AWS WAF
    participant REST as REST API
    participant C as Cognito Authorizer
    participant L as Lambda

    U->>WAF: GET /profile + mismo token del DEMO
    WAF->>REST: trafico valido
    REST->>C: valida token del mismo User Pool
    C-->>REST: token valido
    REST->>L: invoke con claims
    L-->>U: 200

    U->>WAF: GET /health?filter=' or 1=1 --
    WAF-->>U: 403
```

## Que cambia y que no cambia

| Elemento | DEMO | Pagina WAF |
|---|---|---|
| Usuario | igual | igual |
| User Pool | igual | igual |
| Token | igual | igual |
| Tipo de API | HTTP API | REST API |
| Authorizer | JWT Authorizer | Cognito Authorizer |
| WAF | no | si |

## Conclusiones

- El `DEMO` no compite con la pagina WAF; la prepara.
- La pagina WAF no repite el producto; completa la explicacion de seguridad.
- La relacion correcta para un novato es: mismo usuario, mismo token, otra puerta de entrada, segunda capa de defensa.
