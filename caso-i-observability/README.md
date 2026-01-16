# Caso I: Observabilidad y Operaciones - Nivel 8

> **Status**: `PROYECTADO` (Próximamente)

## 🎯 El Desafío
"No puedes mejorar lo que no puedes medir".
Cuando tienes Lambdas, bases de datos y colas (Caso H), ¿cómo sabes dónde falló ese pedido? ¿Cómo sabes si la base de datos está lenta?
El desafío es implementar **Ojos y Oídos** en tu nube.

## 🛠️ Stack Tecnológico
- **Amazon CloudWatch**: Dashboards, Métricas custom y Alarmas.
- **AWS X-Ray**: Trazabilidad distribuida (ver el viaje de una petición entre microservicios).
- **CloudWatch Logs Insights**: Buscador potente para logs.

## 🚀 ¿Qué construiremos?
Instrumentaremos el sistema del Caso D/H para lograr:
1. **Mapa de Servicio**: Ver visualmente cómo se conectan las Lambdas.
2. **Dashboard Ejecutivo**: Ver "Pedidos por minuto" y "Errores" en gráficas en tiempo real.
3. **Alarma Crítica**: Recibir un email si más del 5% de las peticiones fallan en 1 minuto.
