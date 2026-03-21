# Arquitectura: Caso F - identidad primero, perimetro despues

> Stack: Cognito User Pool + HTTP API + JWT Authorizer + REST API + Cognito Authorizer + AWS WAF + AWS SAM
> Nivel: 5 - Identidad administrada y defensa perimetral

---

## Vision general

El Caso F cuenta una sola historia tecnica, pero la reparte en dos puertas de entrada:

- el `DEMO` prueba identidad, login y acceso privado
- la pagina WAF prueba perimetro y bloqueo de trafico sospechoso

No son dos productos distintos. Son dos despliegues coordinados del mismo aprendizaje.

La razon tecnica es concreta:

- `HTTP API` es la forma mas barata y clara de mostrar `JWT Authorizer` nativo
- `AWS WAF` se asocia a `REST API`, no al mismo front door que usamos para el `DEMO`

---

## Que cambio con la version actual

Este documento si debia cambiar con los ultimos ajustes del Caso F.

La arquitectura correcta ahora es:

- la pagina WAF ya no crea otro `User Pool`
- la pagina WAF reutiliza el mismo `User Pool` y el mismo `App Client` del `DEMO`
- el mismo `idToken` emitido en el `DEMO` debe funcionar en `/profile` del WAF
- el WAF queda como capa opcional y costosa, no como producto paralelo

Si el diagrama mostrara dos identidades separadas o una sola API con WAF encima del `HTTP API`, quedaria desactualizado.

---

## Diagrama 1: Producto completo

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#7b2ff7', 'edgeColor': '#4cc9f0', 'tertiaryColor': '#f6f8ff', 'fontSize': '16px' }}}%%
graph TB
    subgraph Client["Cliente"]
        U["Usuario / navegador"]
    end

    subgraph Identity["Identidad compartida"]
        C["Cognito User Pool<br/>App Client sin secreto"]
        P["Lambda Pre-SignUp<br/>solo en DEMO"]
    end

    subgraph Demo["Stack 1: DEMO principal"]
        DAPI["HTTP API"]
        DJ["JWT Authorizer"]
        DL["Lambda SecurityFunction<br/>stack demo"]
    end

    subgraph Perimeter["Stack 2: WAF asociado"]
        W["AWS WAF<br/>Common + SQLi rules"]
        RAPI["REST API"]
        CA["Cognito Authorizer"]
        WL["Lambda SecurityFunction<br/>stack WAF"]
    end

    U --> DAPI
    DAPI -->|register / login| DL
    DAPI -->|profile| DJ
    DJ -. valida JWT contra .-> C
    DJ --> DL
    DL -->|sign_up / initiate_auth| C
    C -. trigger de alta .-> P

    U --> W
    W --> RAPI
    RAPI -->|profile| CA
    RAPI -->|health publico| WL
    CA -. valida el mismo token .-> C
    CA --> WL

    style Identity fill:#E8F5E9,stroke:#43A047,stroke-width:2px
    style Demo fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    style Perimeter fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px
    style Client fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
```

---

## Diagrama 2: Flujo del DEMO

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#c77dff', 'edgeColor': '#7ef0b8', 'tertiaryColor': '#f7f3ff' }}}%%
sequenceDiagram
    participant U as Usuario
    participant HTTP as HTTP API
    participant L as Lambda demo
    participant C as Cognito
    participant J as JWT Authorizer

    U->>HTTP: POST /auth/register
    HTTP->>L: invoca handler publico
    L->>C: sign_up(email, password)
    C-->>L: usuario creado
    L-->>U: 201 + userSub

    U->>HTTP: POST /auth/login
    HTTP->>L: invoca handler publico
    L->>C: initiate_auth
    C-->>L: idToken + accessToken
    L-->>U: 200 + tokens

    U->>HTTP: GET /profile + Bearer idToken
    HTTP->>J: valida issuer / audience / firma
    J-->>HTTP: claims validos
    Note over J,L: La validacion ocurre antes de la logica de negocio
    HTTP->>L: invoca handler protegido
    L-->>U: 200 + perfil
```

---

## Diagrama 3: Flujo del WAF con el mismo token

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#56d364', 'edgeColor': '#0ea5a0', 'tertiaryColor': '#f3fff8' }}}%%
sequenceDiagram
    participant U as Usuario
    participant DEMO as DEMO ya autenticado
    participant WAF as AWS WAF
    participant REST as REST API
    participant A as Cognito Authorizer
    participant C as Cognito compartido
    participant L as Lambda waf

    U->>DEMO: copia el mismo idToken
    U->>WAF: GET /profile + mismo idToken
    WAF->>REST: request permitida
    REST->>A: authorizer nativo
    A->>C: valida token en el mismo User Pool
    C-->>A: token valido
    A-->>REST: claims
    REST->>L: invoca handler protegido
    L-->>U: 200 + mismo perfil

    U->>WAF: GET /health?filter=' or 1=1 --
    WAF-->>U: 403 antes de REST API y Lambda
```

---

## Diagrama 4: Por que existen dos URLs

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#4cc9f0', 'edgeColor': '#4361ee', 'tertiaryColor': '#f5f9ff' }}}%%
graph LR
    subgraph DemoChoice["URL 1: DEMO principal"]
        H1["HTTP API"]
        H2["JWT Authorizer nativo"]
        H3["Costo base practicamente cero"]
        H4["Ideal para registro, login y /profile"]
        H1 --> H2 --> H3 --> H4
    end

    subgraph WafChoice["URL 2: WAF asociado"]
        R1["REST API"]
        R2["Cognito Authorizer"]
        R3["Asociacion con AWS WAF"]
        R4["Ideal para evidencia 403 y perimetro"]
        R1 --> R2 --> R3 --> R4
    end

    S["Mismo User Pool<br/>mismo usuario<br/>mismo token"] --> DemoChoice
    S --> WafChoice

    style DemoChoice fill:#EEF2FF,stroke:#4361EE,stroke-width:2px
    style WafChoice fill:#ECFDF5,stroke:#10B981,stroke-width:2px
```

---

## Claves de diseno

| Decision | Motivo |
|---|---|
| `User Pool` compartido entre ambos stacks | Refuerza que no hay dos productos ni dos identidades separadas |
| `HTTP API` para el `DEMO` | Es la forma mas simple y barata de ensenar `JWT Authorizer` nativo |
| `REST API` para el WAF | Permite asociar `AWS WAF` y mostrar defensa perimetral real |
| Dos Lambdas desplegadas desde el mismo codigo fuente | Mantiene comportamiento coherente sin mezclar responsabilidades en una sola URL |
| `Pre-SignUp` solo en el `DEMO` | El alta de usuarios pertenece a la capa de identidad, no al stack WAF |
| Reutilizar el mismo `idToken` en ambas paginas | Hace visible la diferencia entre autenticacion y perimetro |
| Mantener `VISUALIZATION.md` aunque exista el `DEMO` | El WAF tiene costo fijo y puede destruirse despues de capturas |

---

## Que debe mirar un novato primero

1. abrir el `DEMO`
2. crear usuario y hacer login
3. llamar a `/profile`
4. copiar el mismo `idToken`
5. abrir la pagina WAF
6. probar `/profile` con el mismo token
7. ejecutar la prueba SQLi controlada y observar el `403`

Si ese recorrido no se entiende en ese orden, la arquitectura esta mal contada.

---

## Que demuestra esta arquitectura

- identidad administrada por AWS en vez de autenticacion casera
- validacion de token antes de Lambda
- separacion clara entre autenticacion y perimetro
- criterio FinOps: dejar estable el `DEMO` y tratar el WAF como capa temporal de evidencia

---

## Siguiente paso natural

Las extensiones mas logicas despues de este caso serian:

- agregar metricas de autenticacion y bloqueos WAF al Caso H
- incorporar secretos rotados o MFA como mejora futura
- conectar esta base de identidad con un caso que exponga usuarios reales en otra API
