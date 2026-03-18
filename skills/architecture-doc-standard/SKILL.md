---
name: architecture-doc-standard
description: Estandar obligatorio para crear o corregir el archivo docs/architecture.md de cualquier caso de este monorepo. Usar cuando se crea un caso nuevo, cuando se revisa que un architecture.md existente cumple el estandar, o cuando se detecta que el documento no tiene los 4 diagramas Mermaid requeridos.
---

# Architecture Doc Standard

Cada `caso-X-nombre/docs/architecture.md` en este repositorio sigue un estandar fijo de 8 secciones.
Desviarse del estandar genera inconsistencia entre casos y dificulta la lectura para reclutadores.

---

## Estructura obligatoria (8 secciones en orden)

### Seccion 1 — Cabecera H1

```markdown
# [emoji] Caso X — Nombre Completo del Caso
```

El emoji representa el concepto central del caso:
- Hosting / estatico: 🌐
- IaC / Terraform: 🏗️
- Serverless / Lambda: ⚡
- Seguridad / auth: 🔐
- Observabilidad: 📊
- Contenedores: 🐳
- Kubernetes: ☸️
- FinOps / costos: 💰
- Eventos / async: 📨
- Resiliencia: 🛡️

### Seccion 2 — Bloque de metadata (blockquote)

```markdown
> **Stack:** Lista de servicios AWS principales
> **Nivel:** Numero del nivel (1-11) — Descripcion breve del nivel
> **Estado:** ✅ COMPLETADO | 🔄 EN PROGRESO | ⏳ PROYECTADO
> **Region:** us-east-2
> **Ultima actualizacion:** DD de mes de YYYY
```

### Seccion 3 — Vision general

Parrafo de 3-5 lineas que responde: que hace el caso, por que es importante en la progresion del repositorio, que problema resuelve que los casos anteriores no resolvian.

### Seccion 4 — Los 4 diagramas Mermaid

Esta es la seccion mas importante. Cada caso tiene exactamente 4 diagramas. Los 4 deben ser COMPLEMENTARIOS, no redundantes: cada uno muestra una dimension diferente del mismo sistema.

#### Diagrama 1 — Flujo de interaccion (sequenceDiagram o flowchart TD)

Muestra el flujo de una peticion real de principio a fin. Para casos con usuario → API → backend → datos:

```markdown
## Diagrama 1: Flujo de Interaccion

sequenceDiagram
    actor Usuario
    participant API as API Gateway
    participant Lambda
    participant DB as DynamoDB
    Usuario->>API: POST /endpoint
    API->>Lambda: invoca
    Lambda->>DB: operacion
    DB-->>Lambda: respuesta
    Lambda-->>API: 200 OK
    API-->>Usuario: JSON
```

Para casos de seguridad: mostrar el flujo de autenticacion completo.
Para casos de eventos: mostrar el flujo productor → bus → consumidor.
Para casos de contenedores: mostrar el flujo cliente → ALB → ECS → respuesta.

#### Diagrama 2 — Arquitectura de capas o defensa (flowchart TD)

Muestra las capas del sistema de afuera hacia adentro. Para casos de seguridad: capas de defensa (WAF → API GW → Cognito → Lambda). Para casos de infraestructura: capas de red (Internet → ALB → Fargate → VPC privada). Para casos de observabilidad: los tres pilares (metricas, logs, trazas).

```markdown
## Diagrama 2: Arquitectura de Capas

flowchart TD
    Internet([Internet]) --> Capa1[Capa Exterior]
    Capa1 --> Capa2[Capa Media]
    Capa2 --> Capa3[Capa Interior]
    Capa3 --> Datos[(Almacenamiento)]

    style Capa1 fill:#color1,color:#fff
    style Capa2 fill:#color2,color:#fff
    style Capa3 fill:#color3,color:#fff
```

Usar colores distintos por capa para hacerlo visualmente util.

#### Diagrama 3 — Stack completo IaC (flowchart LR)

Muestra todos los recursos AWS del template.yaml o main.tf como un grafo horizontal (izquierda a derecha). Cada recurso es un nodo. Las flechas muestran dependencias o flujo de datos.

```markdown
## Diagrama 3: Stack Completo

flowchart LR
    CF[CloudFormation Stack] --> API[HttpApi]
    CF --> Lambda[Function]
    CF --> DB[DynamoDB Table]
    API -->|invoca| Lambda
    Lambda -->|lee/escribe| DB
```

Este diagrama debe incluir TODOS los recursos del template, incluyendo los condicionales (indicarlos con nota).

#### Diagrama 4 — Decision tecnica o comparativa (flowchart TD o tabla visual)

Muestra por que se eligio una solucion sobre otra. Ejemplos:
- JWT Authorizer nativo vs Custom Authorizer Lambda (Caso F)
- DynamoDB Single Table vs Multi-Table (Caso E)
- ECS Fargate vs Lambda para este caso especifico (Caso J)
- CloudWatch Dashboard IaC vs manual (Caso H)
- OIDC vs Access Keys permanentes (Caso L)

```markdown
## Diagrama 4: Decision de Diseno

flowchart TD
    Problema[Necesidad: autenticacion] --> OpcionA[Opcion A: Lambda custom]
    Problema --> OpcionB[Opcion B: JWT Authorizer nativo]
    OpcionA --> ContraA[Codigo adicional, latencia +20ms, costo extra]
    OpcionB --> VentajaB[Sin codigo criptografico, validacion RS256 nativa, gratis]
    VentajaB --> Elegido[✅ Elegido para este caso]

    style Elegido fill:#2ea043,color:#fff
    style ContraA fill:#da3633,color:#fff
```

### Seccion 5 — Tabla de componentes

```markdown
## Componentes principales

| Componente | Servicio AWS | Rol en la arquitectura | Costo |
|---|---|---|---|
| API REST | API Gateway HTTP | Punto de entrada | Free tier |
| Logica | Lambda Python 3.12 | Procesamiento | Free tier |
| Datos | DynamoDB | Persistencia | Free tier |
```

La columna Costo debe ser honesta: "Free tier", "~$3/mes si activo", "$72/mes — destruir".

### Seccion 6 — Tabla de decisiones de diseno

Minimo 5 entradas, idealmente 7.

```markdown
## Decisiones de diseno

| Decision | Alternativa descartada | Razon |
|---|---|---|
| JWT Authorizer nativo | Lambda custom authorizer | Sin codigo criptografico, validacion RS256 sin costo extra |
| DynamoDB PAY_PER_REQUEST | Provisioned capacity | Escala a cero — ideal para laboratorio |
| Python 3.12 | Node.js | Consistencia con el resto de casos serverless del repositorio |
```

### Seccion 7 — Que aprende un reclutador

```markdown
## Que aprende un reclutador de este caso

- **Punto 1**: habilidad tecnica concreta demostrada
- **Punto 2**: decision de arquitectura que muestra criterio senior
- **Punto 3**: conocimiento de AWS que diferencia al candidato
- **Punto 4**: practica de seguridad o FinOps aplicada
- **Punto 5**: capacidad de testing o documentacion
```

Minimo 5 puntos. Redactar en terminos de valor para el negocio, no solo tecnicos.

### Seccion 8 — Siguiente paso natural y referencias

```markdown
## Siguiente paso natural

[Nombre del caso o concepto] — [por que es la evolucion logica de este caso]

## Referencias

- [Nombre del servicio — AWS Docs](URL)
- [Nombre del servicio — AWS Docs](URL)
```

Minimo 3 referencias. Usar siempre URLs de documentacion oficial de AWS.

---

## Lista de verificacion antes de hacer commit

- [ ] Tiene los 8 secciones en orden
- [ ] Tiene exactamente 4 diagramas Mermaid numerados
- [ ] Los 4 diagramas son complementarios (no repiten la misma informacion)
- [ ] El Diagrama 3 incluye todos los recursos del template.yaml
- [ ] El Diagrama 4 justifica al menos una decision tecnica real del caso
- [ ] La tabla de componentes tiene la columna Costo con valores reales
- [ ] La tabla de decisiones tiene minimo 5 entradas
- [ ] La seccion de reclutador tiene minimo 5 puntos en lenguaje de negocio
- [ ] Hay minimo 3 referencias a documentacion oficial de AWS

---

## Casos de referencia para revisar antes de crear un architecture.md nuevo

Leer primero el mas cercano en tipo:
- Caso serverless simple: `caso-d-serverless-basic/docs/architecture.md`
- Caso con DynamoDB avanzado: `caso-e-dynamodb-persistence/docs/architecture.md`
- Caso de seguridad: `caso-f-security-cognito/docs/architecture.md`
- Caso de eventos: `caso-g-event-driven/docs/architecture.md`
- Caso de observabilidad: `caso-h-observability/docs/architecture.md`
- Caso de contenedores: `caso-j-containers-ecs/docs/architecture.md`
