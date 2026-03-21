# Arquitectura: Caso F - DEMO principal + pagina WAF auxiliar

## Idea central

El Caso F tiene un solo producto principal:

- `DEMO` con Cognito + HTTP API + JWT Authorizer

Y un despliegue complementario:

- pagina WAF auxiliar con REST API + WAF para explicar y validar el perimetro

`VISUALIZATION.md` no es otro despliegue. Es la bitacora de costo y cierre seguro del stack WAF.

## Por que se separa

- `HTTP API` es la opcion mas barata y simple para el DEMO
- `AWS WAF` se asocia a `REST API`
- separar el perimetro en una pagina auxiliar evita confundir el producto principal

## Diagrama 1: Vista general

```mermaid
flowchart TD
    Product["DEMO principal"]
    Product --> Demo["HTTP API<br/>JWT Authorizer<br/>Cognito"]

    Product --> Link["Enlace visible al despliegue WAF"]
    Link --> Waf["REST API<br/>WAF<br/>Pagina auxiliar"]

    Waf --> Cost["VISUALIZATION.md<br/>costo y destruccion"]
```

## Diagrama 2: Flujo del DEMO

```mermaid
sequenceDiagram
    actor U as Usuario
    participant APIGW as API Gateway HTTP API
    participant L as Lambda
    participant C as Cognito

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

## Diagrama 3: Flujo de la pagina WAF

```mermaid
sequenceDiagram
    actor U as Usuario
    participant W as AWS WAF
    participant APIGW as API Gateway REST API
    participant L as Lambda

    U->>W: GET /health
    W->>APIGW: trafico normal
    APIGW->>L: invoke
    L-->>U: 200

    U->>W: GET /health?filter=' or 1=1 --
    W-->>U: 403
```

## Que resuelve cada pieza

| Pieza | Rol |
|---|---|
| `template.yaml` | producto principal del caso |
| `template-visualization.yaml` | pagina WAF enlazada desde el DEMO |
| `VISUALIZATION.md` | control de costo y destruccion del stack WAF |

## Resultado esperado

- el usuario entiende el producto apenas abre el DEMO
- el DEMO muestra el flujo funcional completo
- el enlace WAF abre una pagina separada y explicativa
- el stack WAF se destruye despues de la ventana de evidencia
