# Guia para Reclutadores y Evaluadores Tecnicos

> **Proposito**: ayudar a entender rapidamente el valor tecnico y de negocio de este monorepo, con foco en decisiones arquitectonicas reales y capacidades ya demostradas.

---

## Resumen ejecutivo

**Proyectos AWS GitLab** es un monorepo profesional que muestra la evolucion de un perfil cloud desde hosting estatico hasta contenedores, Kubernetes, FinOps y persistencia NoSQL avanzada.

Lo importante no es solo la variedad de tecnologias, sino que varios casos ya estan **desplegados, validados y documentados con evidencia operativa**.

- **Arquitectura**: progresion desde hosting simple hasta plataformas multi-servicio.
- **IaC**: uso de Terraform y AWS SAM.
- **CI/CD**: GitLab integrado con AWS.
- **Seguridad**: escaneo de secretos, minimo privilegio y direccion hacia OIDC.
- **Datos**: DynamoDB modelado por patrones de acceso, no como traduccion directa de SQL.

---

## Valor de negocio

| Pilar | Beneficio para el negocio | Implementacion visible |
| :--- | :--- | :--- |
| **Agilidad** | Despliegues rapidos y repetibles | Pipelines y guias operativas por caso |
| **Seguridad** | Menor riesgo de errores manuales y fugas | Validaciones, IAM y documentacion de hardening |
| **Costo** | Uso eficiente de recursos administrados | Amplify, Lambda, DynamoDB On-Demand, hibernacion FinOps |
| **Escalabilidad** | Respuesta elastica segun el tipo de carga | CloudFront, Lambda, ECS y EKS |
| **Persistencia** | Diseños de datos pensados para consultas reales | Caso E con Single Table Design y GSIs |
| **Integracion asincrona** | Sistemas menos acoplados y mas tolerantes a picos y errores | Caso G con EventBridge, SQS, DLQ y SNS |

---

## Decisiones tecnicas clave

### 1. Monorepo evolutivo

Cada carpeta representa una capacidad concreta y acumulativa. No son demos desconectadas, sino una progresion:

- hosting y deploy
- IaC y backend
- persistencia avanzada
- contenedores y orquestacion
- FinOps y resiliencia

### 2. Infraestructura declarativa

- **Terraform** para infraestructura tradicional e industrial
- **AWS SAM** para serverless y APIs

### 3. Persistencia modelada por acceso

El `Caso E` es especialmente relevante para evaluacion senior porque demuestra algo que suele faltar en portafolios: **diseño NoSQL real**.

Incluye:

- DynamoDB con tabla unica
- GSIs para lectura por estado y producto
- escritura transaccional de orden y auditoria
- validacion operativa con API publica y landing de demostracion

### 4. Direccion de seguridad correcta

El repositorio apunta a operar con credenciales temporales y controles cada vez mas fuertes, reduciendo dependencia de llaves permanentes.

---

## Casos destacados

### Caso C: Infraestructura como codigo (Terraform)

**Problema**: despliegues manuales poco auditables.
**Solucion**: Terraform con estado remoto y distribucion global con CloudFront.
**Habilidad demostrada**: IaC, AWS networking, control declarativo.

### Caso D: Serverless API

**Problema**: backend que consume recursos aunque no haya trafico.
**Solucion**: API Gateway + Lambda + DynamoDB.
**Habilidad demostrada**: arquitectura serverless y backend en AWS.

### Caso E: Persistence Pro

**Problema**: muchos proyectos usan DynamoDB como si fuera una base relacional sin estrategia de acceso.
**Solucion**: modelado por patrones de consulta, indices globales y auditoria transaccional.
**Habilidad demostrada**: NoSQL design, serverless data modeling y criterio arquitectonico.
**Estado**: desplegado y validado en AWS.
**Demo**: [API + landing publica](https://gqqm27j47c.execute-api.us-east-2.amazonaws.com/)

### Caso G: Event Driven

**Problema**: una API sincrona puede quedar lenta o fragil cuando intenta hacer too much trabajo en la misma llamada.
**Solucion**: aceptar el evento, publicarlo en EventBridge, amortiguarlo con SQS, procesarlo fuera de banda y aislar errores con DLQ.
**Habilidad demostrada**: event-driven design, desacoplamiento, reintentos, DLQ y lectura operativa del flujo.
**Estado**: desplegado y validado en AWS.
**Demo**: [Landing + API publica](https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/)

### Caso K: Kubernetes en AWS

**Problema**: gestionar contenedores a escala con estandares abiertos.
**Solucion**: despliegue real en EKS con balanceo y self-healing.
**Habilidad demostrada**: Kubernetes, EKS y operacion cloud nativa.

### Caso L: FinOps y governance

**Problema**: credenciales permanentes y costos sin control.
**Solucion**: presupuestos, gobernanza y direccion hacia OIDC.
**Habilidad demostrada**: costo, seguridad y operacion responsable.

---

## Que diferencia este portafolio

- No se queda en infraestructura basica; incluye datos, costos y operacion.
- No documenta solo aspiraciones; varios casos estan ya publicados y verificables.
- El `Caso E` agrega una capa de madurez poco comun: persistencia NoSQL orientada a negocio.
- El `Caso G` suma una segunda capa de criterio senior: procesamiento asincrono y tolerancia a fallos sin romper la API de entrada.

---

## Tour guiado sugerido

1. [README.md](../README.md)
2. [docs/ARCHITECTURE.md](./ARCHITECTURE.md)
3. [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md)
4. [caso-g-event-driven/README.md](../caso-g-event-driven/README.md)
5. [caso-g-event-driven/docs/architecture.md](../caso-g-event-driven/docs/architecture.md)
6. [caso-g-event-driven/AWS_PASO_A_PASO.md](../caso-g-event-driven/AWS_PASO_A_PASO.md)

---

## Habilidades demostradas

- **Cloud Computing**: AWS aplicado a multiples patrones
- **IaC**: Terraform y CloudFormation/SAM
- **Backend**: APIs serverless y persistencia NoSQL
- **Containers**: Docker, ECS y EKS
- **FinOps y seguridad**: presupuestos, IAM, escaneo y controles operativos
- **Comunicacion tecnica**: documentacion amplia, trazable y orientada a distintos lectores

---

_Ultima actualizacion: 2026-03-12_

