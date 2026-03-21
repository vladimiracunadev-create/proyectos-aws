# Guia para Reclutadores y Evaluadores Tecnicos

> **Proposito**: ayudar a entender rapidamente el valor tecnico y de negocio de este monorepo, con foco en decisiones arquitectonicas reales y capacidades ya demostradas.

---

## Resumen ejecutivo

**Proyectos AWS GitLab** es un monorepo profesional que muestra la evolucion de un perfil cloud desde hosting estatico hasta seguridad perimetral, observabilidad como codigo, contenedores, Kubernetes y FinOps.

Lo importante no es solo la variedad de tecnologias, sino que **11 casos ya estan completados**, varios de ellos **desplegados, validados y documentados con evidencia operativa**.

- **Arquitectura**: progresion desde hosting simple hasta plataformas multi-servicio con identidad y perimetro.
- **IaC**: uso de Terraform y AWS SAM. Todo recurso relevante tiene definicion declarativa.
- **CI/CD**: GitLab integrado con AWS, incluyendo test jobs por caso y stages de seguridad.
- **Seguridad**: autenticacion con Cognito + JWT Authorizer nativo, WAF opcional, escaneo de secretos, minimo privilegio y OIDC.
- **Datos**: DynamoDB modelado por patrones de acceso, no como traduccion directa de SQL.
- **Observabilidad**: dashboards CloudWatch como codigo, alarmas proactivas y trazas X-Ray.

---

## Valor de negocio

| Pilar | Beneficio para el negocio | Implementacion visible |
| :--- | :--- | :--- |
| **Agilidad** | Despliegues rapidos y repetibles | Pipelines y guias operativas por caso |
| **Seguridad** | Identidad gestionada, perimetro declarativo | Caso F: Cognito + JWT Authorizer + WAF |
| **Costo** | Uso eficiente de recursos administrados | Amplify, Lambda, DynamoDB On-Demand, FinOps |
| **Escalabilidad** | Respuesta elastica segun el tipo de carga | CloudFront, Lambda, ECS y EKS |
| **Persistencia** | Diseños de datos pensados para consultas reales | Caso E: Single Table Design y GSIs |
| **Integracion asincrona** | Sistemas menos acoplados y mas tolerantes a errores | Caso G: EventBridge, SQS, DLQ y SNS |
| **Observabilidad** | Deteccion proactiva antes que el usuario | Caso H: CloudWatch Dashboard IaC + X-Ray + Alarmas |

---

## Decisiones tecnicas clave

### 1. Monorepo evolutivo

Cada carpeta representa una capacidad concreta y acumulativa. No son demos desconectadas, sino una progresion:

- hosting y deploy
- IaC y backend
- persistencia avanzada
- integracion asincrona
- seguridad perimetral e identidad
- observabilidad como codigo
- contenedores y orquestacion
- FinOps y resiliencia

### 2. Infraestructura declarativa

- **Terraform** para infraestructura tradicional e industrial
- **AWS SAM** para serverless y APIs
- **CloudFormation inline** para dashboards y alarmas (Caso H)

### 3. Persistencia modelada por acceso

El `Caso E` es especialmente relevante para evaluacion senior porque demuestra algo que suele faltar en portafolios: **diseño NoSQL real**.

Incluye:

- DynamoDB con tabla unica
- GSIs para lectura por estado y producto
- escritura transaccional de orden y auditoria
- validacion operativa con API publica y landing de demostracion

### 4. Seguridad sin codigo de criptografia

El `Caso F` muestra un patron maduro: el JWT Authorizer nativo de API Gateway valida la firma RS256, el issuer y el audience de Cognito **antes de invocar la Lambda**. La Lambda solo lee claims ya validados. Cero codigo de criptografia propio.

### 5. Observabilidad como codigo

El `Caso H` no crea el dashboard desde la consola: el `AWS::CloudWatch::Dashboard` nace con el SAM stack y muere con el. Las alarmas sobre errores Lambda y latencia p99 estan definidas declarativamente. Igual que la infraestructura.

---

## Casos destacados

### Caso C: Infraestructura como codigo (Terraform)

**Problema**: despliegues manuales poco auditables.
**Solucion**: Terraform con estado remoto y distribucion global con CloudFront y OAC.
**Habilidad demostrada**: IaC, AWS networking, control declarativo.

### Caso E: Persistence Pro

**Problema**: muchos proyectos usan DynamoDB como si fuera una base relacional sin estrategia de acceso.
**Solucion**: modelado por patrones de consulta, indices globales y auditoria transaccional.
**Habilidad demostrada**: NoSQL design, serverless data modeling y criterio arquitectonico.
**Estado**: desplegado y validado en AWS.
**Demo**: [API + landing publica](https://gqqm27j47c.execute-api.us-east-2.amazonaws.com/)

### Caso F: Security First (Cognito + JWT + WAF)

**Problema**: APIs publicas sin autenticacion ni perimetro.
**Solucion**: Cognito User Pool para identidades, JWT Authorizer nativo en API Gateway para autorizacion sin codigo Lambda, WAF opcional para bloquear SQLi y XSS.
**Habilidad demostrada**: identidad en AWS, defensa en profundidad, IaC de seguridad, separacion autenticacion/autorizacion.
**Estado**: completado con tests y documentacion.
**Demo**: [DEMO principal](https://tmi7kgebl9.execute-api.us-east-2.amazonaws.com/) / [WAF asociado](https://2i88ijfu54.execute-api.us-east-2.amazonaws.com/Prod)
**Respaldo FinOps**: [Reporte de Visualizacion y Resultados](../caso-f-security-cognito/VISUALIZATION.md)

### Caso G: Event Driven

**Problema**: una API sincrona puede quedar lenta o fragil cuando intenta hacer demasiado trabajo en la misma llamada.
**Solucion**: aceptar el evento, publicarlo en EventBridge, amortiguarlo con SQS, procesarlo fuera de banda y aislar errores con DLQ.
**Habilidad demostrada**: event-driven design, desacoplamiento, reintentos, DLQ y lectura operativa del flujo.
**Estado**: desplegado y validado en AWS.
**Demo**: [Landing + API publica](https://ajcjvroq0a.execute-api.us-east-2.amazonaws.com/)

### Caso H: Observability & Health

**Problema**: no saber que falla hasta que el usuario se queja.
**Solucion**: CloudWatch Dashboard definido como codigo en SAM, alarmas sobre errores Lambda y latencia p99, metricas custom, trazas X-Ray en todas las invocaciones.
**Habilidad demostrada**: los tres pilares de observabilidad (metricas, logs, trazas), IaC de monitorizacion, diferencia entre metricas tecnicas y de negocio.
**Estado**: validado en AWS y retirado despues de la captura por costos FinOps.
**Evidencia**: [Reporte de Visualizacion y Resultados](../caso-h-observability/VISUALIZATION.md)
**Ultima URL validada (historica)**: [https://z7evf8mrzf.execute-api.us-east-2.amazonaws.com/](https://z7evf8mrzf.execute-api.us-east-2.amazonaws.com/)
**Nota FinOps**: el dashboard CloudWatch tiene costo fijo, por eso la demo se levanta por ventanas controladas y luego se destruye.

### Caso K: Kubernetes en AWS

**Problema**: gestionar contenedores a escala con estandares abiertos.
**Solucion**: despliegue real en EKS con balanceo y self-healing.
**Habilidad demostrada**: Kubernetes, EKS y operacion cloud nativa.

### Caso L: FinOps y governance

**Problema**: credenciales permanentes y costos sin control.
**Solucion**: presupuestos AWS Budgets, gobernanza IAM y autenticacion OIDC Zero-Trust.
**Habilidad demostrada**: costo, seguridad y operacion responsable.

---

## Que diferencia este portafolio

- No se queda en infraestructura basica; incluye datos, seguridad, observabilidad, costos y operacion.
- No documenta solo aspiraciones; varios casos estan ya publicados y verificables con URL activa.
- El `Caso F` agrega autenticacion sin codigo de criptografia: un patron que diferencia a perfiles cloud maduros.
- El `Caso H` muestra que la observabilidad es codigo, no configuracion manual posterior al deploy.
- 60+ tests unitarios cubren todas las Lambdas — pipeline CI/CD verde en cada push.
- El repositorio soporta preparacion para certificaciones AWS: SAA-C03, DVA-C02 y SOA-C02 (ver `docs/cert-*.md`).

---

## Tour guiado sugerido

1. [README.md](../README.md) — vision global y mapa de relaciones entre casos
2. [docs/ARCHITECTURE.md](./ARCHITECTURE.md) — evolucion por tiers
3. [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md) — persistencia NoSQL
4. [caso-f-security-cognito/docs/architecture.md](../caso-f-security-cognito/docs/architecture.md) — seguridad como IaC
5. [caso-g-event-driven/README.md](../caso-g-event-driven/README.md) — arquitectura event-driven
6. [caso-h-observability/docs/architecture.md](../caso-h-observability/docs/architecture.md) — observabilidad como codigo

---

## Habilidades demostradas

- **Cloud Computing**: AWS aplicado a multiples patrones arquitectonicos
- **IaC**: Terraform y CloudFormation/SAM para infraestructura, seguridad y observabilidad
- **Backend**: APIs serverless, persistencia NoSQL y arquitectura event-driven
- **Seguridad**: Cognito, JWT Authorizer, WAF, IAM, escaneo de secretos y OIDC
- **Observabilidad**: CloudWatch Dashboard IaC, alarmas proactivas y trazas X-Ray
- **Containers**: Docker, ECS Fargate y Kubernetes EKS
- **FinOps**: presupuestos, gobernanza y controles de costo
- **Testing**: 60+ tests unitarios con pytest, CI jobs por caso y smoke tests post-deploy
- **Comunicacion tecnica**: documentacion amplia, trazable y orientada a distintos lectores

---

_Ultima actualizacion: 2026-03-20_
