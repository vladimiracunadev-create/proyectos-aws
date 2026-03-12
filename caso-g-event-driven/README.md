# Caso G: Event Driven (Arquitectura Asincrona)

[![Nivel-6](https://img.shields.io/badge/Nivel-6_Eventos-yellow?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Validado-success?style=for-the-badge)]()

Este caso lleva la plataforma desde la persistencia sincrona del Caso E hacia una
arquitectura desacoplada basada en eventos. En vez de encadenar servicios con llamadas
directas, una Lambda publica eventos de negocio en **Amazon EventBridge**, una regla los
enruta a **Amazon SQS**, y otra Lambda los procesa de forma asincrona con soporte para
**DLQ** y notificacion por **SNS**.

---

## Estado real

Estado actual del repositorio y de AWS:

- El caso ya no esta vacio: ahora existe un modulo tecnico completo y desplegado.
- La infraestructura **AWS SAM** fue desplegada y validada en AWS el **12 de marzo de 2026**.
- La URL base operativa es `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com`.
- La raiz `/` expone una landing interactiva para explicar el despliegue y probar el flujo.
- El bus desplegado es `caso-g-orders-bus`.
- La cola principal es `orders-processing-queue`.
- La DLQ es `orders-processing-dlq`.
- El topic SNS desplegado es `arn:aws:sns:us-east-2:689978033715:processing-notifications`.

Validacion completada:

1. `sam build` ejecutado con exito.
2. Stack `caso-g-event-driven` desplegado en `us-east-2`.
3. Validada la landing publica en `GET /`.
4. Validado `GET /health` en modo HTML para navegador y JSON para tooling.
5. Validado `POST /events/orders` con respuesta `202 Accepted`.
6. Confirmado el procesamiento del consumidor Lambda.
7. Confirmada la ruta de error historica hacia DLQ durante la primera iteracion de prueba.

## Objetivo

Demostrar los fundamentos de una arquitectura event-driven moderna:

- publicar eventos de negocio sin acoplar productor y consumidor
- amortiguar carga con colas
- aislar fallos con reintentos y `Dead Letter Queue`
- separar escritura transaccional de procesamiento posterior
- dejar una base natural para el futuro Caso H de observabilidad

## Stack

- **Entrada**: API Gateway HTTP API
- **Productor**: AWS Lambda `OrderPublisherFunction`
- **Bus de eventos**: Amazon EventBridge
- **Buffer y resiliencia**: Amazon SQS + SQS DLQ
- **Consumidor**: AWS Lambda `OrderConsumerFunction`
- **Notificacion**: Amazon SNS
- **IaC**: AWS SAM / CloudFormation

## Endpoint desplegado

- **API Base URL**: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com`
- **Landing publica**: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/`
- **Health HTML**: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/health`
- **Health JSON**: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/health?format=json`
- **Stack**: `caso-g-event-driven`
- **Region**: `us-east-2`
- **Event Bus**: `caso-g-orders-bus`
- **Orders Queue**: `orders-processing-queue`
- **Orders DLQ**: `orders-processing-dlq`

## Flujo de negocio modelado

1. El cliente publica una orden o evento de negocio mediante `POST /events/orders`.
2. La Lambda publicadora valida el payload y ejecuta `PutEvents` sobre un bus custom.
3. EventBridge aplica una regla por `source` y `detail-type`.
4. La regla entrega el evento a una cola SQS.
5. La Lambda consumidora procesa el mensaje de forma asincrona.
6. Si el procesamiento falla varias veces, el mensaje termina en la DLQ.
7. Cuando el procesamiento es exitoso, se publica un resumen en SNS.

## Estructura del caso

```text
caso-g-event-driven/
|- README.md
|- AWS_PASO_A_PASO.md
|- index.html
|- app.js
|- styles.css
|- backend/
|  |- template.yaml
|  |- events/
|  |  |- publish-order.json
|  |- src/
|     |- app.py
|- docs/
   |- architecture.md
```

## Implementacion incluida

### Backend

- `backend/template.yaml`
  Define HTTP API, Event Bus, SQS principal, DLQ, SNS Topic, reglas de EventBridge y las dos Lambdas.
- `backend/src/app.py`
  Implementa:
  - landing HTML explicativa en `GET /`
  - endpoint `GET /health` con vista HTML para navegador y JSON para monitoreo
  - endpoint `POST /events/orders`
  - publicacion en EventBridge
  - consumo de mensajes SQS
  - publicacion de notificacion SNS despues del procesamiento
- `backend/events/publish-order.json`
  Evento listo para `sam local invoke`.

### Frontend local

- `index.html`, `app.js`, `styles.css`
  Landing estatica adicional para explicar el caso, cargar una `API Base URL` y publicar eventos desde el navegador.

## Ejecucion local orientativa

```bash
cd caso-g-event-driven/backend
sam build
sam local start-api
```

Luego abre `caso-g-event-driven/index.html` en un servidor local y apunta a
`http://127.0.0.1:3000`.

## Estado del caso

`COMPLETADO (VALIDADO)`

## Lo que demuestra este caso

- diseno desacoplado entre productor y consumidor
- tolerancia basica a picos de carga con SQS
- manejo de errores con reintentos y DLQ
- eventos de negocio como contrato entre componentes
- una base clara para observabilidad, tracing y metricas futuras
- una lectura mas humana del estado operativo basico via `/health`

---

## Enlaces relacionados

- [Arquitectura Mermaid](./docs/architecture.md)
- [Guia Paso a Paso AWS](./AWS_PASO_A_PASO.md)
- [Caso E - Persistencia previa](../caso-e-dynamodb-persistence/README.md)
- [Arquitectura global](../docs/ARCHITECTURE.md)
