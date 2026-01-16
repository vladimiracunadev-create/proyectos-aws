# Caso H: Arquitecturas Orientadas a Eventos (EDA) - Nivel 7

> **Status**: `PROYECTADO` (Próximamente)

## 🎯 El Desafío
Hasta ahora, tus sistemas (Caso D, E) han sido "síncronos" (A llama a B y espera). En sistemas grandes, esto crea cuellos de botella.
El desafío aquí es **desacoplar** componentes. Que el sistema "reaccione" a cosas que pasan, sin esperas.

## 🛠️ Stack Tecnológico
- **Amazon EventBridge**: El cerebro que enruta eventos.
- **Amazon SQS (Simple Queue Service)**: Cola de mensajes para amortiguar tráfico.
- **Amazon SNS (Simple Notification Service)**: Para broadcasting (enviar a muchos a la vez).

## 🚀 ¿Qué construiremos?
Un sistema de **"Procesamiento de Pedidos Asíncrono"**:
1. Usuario crea pedido (API Gateway).
2. Se confirma al usuario "Recibido" inmediatamente (0 espera).
3. Por detrás, se dispara un evento `OrderPlaced`.
4. Tres servicios distintos reaccionan a la vez:
   - Servicio de Facturación (genera PDF).
   - Servicio de Logística (avisa al almacén).
   - Servicio de Notificación (envía email).
