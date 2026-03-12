# Guia Paso a Paso AWS - Caso G

## 0. Definicion de operativo

Para este repositorio, el Caso G se considerara operativo cuando se cumplan estos puntos:

- `sam build` termina sin errores.
- `sam deploy` crea el stack en AWS.
- El endpoint `POST /events/orders` responde `202 Accepted`.
- El evento aparece en EventBridge y se enruta a SQS.
- La Lambda consumidora procesa el mensaje correctamente.
- Los fallos deliberados terminan en la `Dead Letter Queue`.
- Se documenta la URL final y los nombres reales de bus, cola y topic.

Estado actual validado el **12 de marzo de 2026**:

- `sam build` ejecutado con exito.
- Stack desplegado: `caso-g-event-driven`.
- Region: `us-east-2`.
- API Base URL: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com`.
- Landing publica: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/`.
- Event Bus: `caso-g-orders-bus`.
- Cola principal: `orders-processing-queue`.
- DLQ: `orders-processing-dlq`.
- SNS Topic: `arn:aws:sns:us-east-2:689978033715:processing-notifications`.

---

## 1. Requisitos previos

Necesitas tener instalado:

- AWS CLI configurado con una cuenta valida
- AWS SAM CLI
- Python 3.12 o compatible
- Docker si quieres usar `sam local`

Verifica:

```bash
aws sts get-caller-identity
sam --version
python --version
```

---

## 2. Arquitectura que vas a desplegar

Dentro de `caso-g-event-driven/backend/template.yaml` se crean:

- 1 HTTP API
- 1 landing HTML en la raiz `/`
- 1 EventBridge custom bus
- 1 regla EventBridge para eventos `OrderCreated`
- 1 cola SQS principal
- 1 DLQ
- 1 topic SNS
- 1 Lambda publicadora
- 1 Lambda consumidora

La idea es separar claramente:

- **ingesta** del evento
- **transporte** y enrutamiento
- **procesamiento** asincrono
- **manejo de fallos**

---

## 3. Compilar la aplicacion

```bash
cd caso-g-event-driven/backend
sam build
```

Esto valida la plantilla y empaqueta la Lambda.

---

## 4. Desplegar por primera vez

```bash
sam deploy --guided
```

Valores sugeridos:

- `Stack Name`: `caso-g-event-driven`
- `AWS Region`: `us-east-2`
- `Confirm changes before deploy`: `Y`
- `Allow SAM CLI IAM role creation`: `Y`
- `Disable rollback`: `N`
- `Save arguments to samconfig.toml`: `Y`

Version no interactiva recomendada:

```bash
sam deploy \
  --stack-name caso-g-event-driven \
  --region us-east-2 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset
```

---

## 5. Obtener los outputs

Despues del despliegue, revisa los outputs del stack:

- `ApiBaseUrl`
- `EventBusName`
- `OrdersQueueName`
- `OrdersDlqName`
- `NotificationsTopicArn`

Comando util:

```bash
aws cloudformation describe-stacks \
  --stack-name caso-g-event-driven \
  --query "Stacks[0].Outputs"
```

Outputs reales del despliegue validado:

- `ApiBaseUrl`: `https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com`
- `EventBusName`: `caso-g-orders-bus`
- `OrdersQueueName`: `orders-processing-queue`
- `OrdersDlqName`: `orders-processing-dlq`
- `NotificationsTopicArn`: `arn:aws:sns:us-east-2:689978033715:processing-notifications`

---

## 6. Probar la API en AWS

### Publicar un evento de orden

```bash
curl -X POST "$API_BASE_URL/events/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "ord-1001",
    "customerId": "cust-001",
    "customerName": "Acme SPA",
    "total": 249.90,
    "status": "CREATED",
    "items": [
      { "sku": "sku-erp", "quantity": 1 }
    ]
  }'
```

Respuesta esperada:

- codigo HTTP `202`
- `eventId` generado por EventBridge
- `bus` con el nombre del custom bus

Resultado validado:

- `GET /` expone una landing explicativa para demostrar el caso.
- `GET /health` respondio correctamente.
- `POST /events/orders` respondio `202 Accepted`.
- El consumidor proceso correctamente un evento de prueba.
- La DLQ conserva 1 mensaje historico de la primera prueba fallida antes del fix del consumidor.

### Health check

```bash
curl "$API_BASE_URL/health"
```

### Landing publica

```bash
curl "$API_BASE_URL/"
```

La raiz entrega una pagina HTML que explica:

- que estas desplegando
- por que usar EventBridge + SQS + DLQ
- que problema operativo resuelve
- que consideraciones se agregaron al despliegue
- como probar el flujo en vivo desde la propia API

---

## 7. Verificar el flujo en AWS Console

### EventBridge

1. Abre **Amazon EventBridge**.
2. Entra al bus `caso-g-orders-bus`.
3. Revisa la regla `OrderCreatedRule`.
4. Valida que el patron filtre:
   - `source = caso.g.orders`
   - `detail-type = OrderCreated`

### SQS

1. Abre **Amazon SQS**.
2. Entra a la cola principal.
3. Si el consumidor esta funcionando, la profundidad deberia volver a `0`.
4. Si fuerzas fallos repetidos, revisa la cola DLQ.

### Lambda

1. Abre **AWS Lambda**.
2. Revisa `OrderPublisherFunction`.
3. Revisa `OrderConsumerFunction`.
4. En **Monitor > Logs**, confirma el flujo:
   - evento recibido
   - mensaje procesado
   - publicacion SNS

### SNS

1. Abre **Amazon SNS**.
2. Entra al topic de notificaciones.
3. Si agregas una suscripcion por email, recibirias la confirmacion de procesamiento.

---

## 8. Probar en local con eventos de ejemplo

Desde la carpeta `backend/`:

```bash
sam local invoke OrderPublisherFunction --event events/publish-order.json
```

O levantar la API local:

```bash
sam local start-api
```

Luego prueba:

```bash
curl -X POST http://127.0.0.1:3000/events/orders \
  -H "Content-Type: application/json" \
  -d @events/publish-order.json
```

> Nota: `sam local` es suficiente para validar la API y la logica de publicacion, pero el flujo
> completo EventBridge -> SQS -> Lambda se valida de verdad una vez desplegado en AWS.

---

## 9. Simular errores y DLQ

La Lambda consumidora marca error si el `detail` incluye:

```json
{ "forceFailure": true }
```

Ejemplo:

```bash
curl -X POST "$API_BASE_URL/events/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "ord-fail-001",
    "customerId": "cust-999",
    "status": "CREATED",
    "forceFailure": true
  }'
```

Despues de varios reintentos, el mensaje deberia terminar en la DLQ.

---

## 10. Frontend local para demo

El caso incluye una landing local en:

- `caso-g-event-driven/index.html`

Uso recomendado:

1. Levanta la API local o despliegala en AWS.
2. Abre la landing con un servidor local.
3. Pega la `API Base URL`.
4. Publica eventos de ejemplo desde el formulario.
5. Revisa el resultado JSON en pantalla.

---

## 11. Limpieza

Cuando termines el laboratorio:

```bash
sam delete --stack-name caso-g-event-driven --region us-east-2
```

Esto elimina API Gateway, Lambdas, EventBridge resources, SQS y SNS.

---

## 12. Siguiente paso natural

La evolucion natural de este caso es:

- agregar metrica de negocio y latencia en CloudWatch
- incorporar tracing y correlacion de eventos
- crear dashboards y alarmas sobre DLQ
- conectar estos indicadores al futuro **Caso H - Observability**
