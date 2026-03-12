# Manual de Aprendizaje: La Guia del Novato

Bienvenido. Si estas aqui, es porque quieres entender que hay "bajo el capo" de este proyecto. Piensa en este repositorio como un **gimnasio de arquitectura cloud**. Cada carpeta es una maquina de ejercicios distinta que te prepara para retos reales en AWS.

---

## Los fundamentos: que estamos usando

1. **Git**: Guarda el historial de todo para poder volver atras si rompemos algo.
2. **GitLab**: Aloja el codigo y ejecuta robots de `CI/CD`.
3. **AWS**: Es el terreno donde viven las apps y servicios (`S3`, `Lambda`, `CloudFront`, `DynamoDB`, `EKS`).
4. **Makefile**: Resume comandos largos en atajos faciles.
5. **Docker**: Permite que el proyecto funcione igual en distintas maquinas.

---

## Deep dive: analisis de los casos

A medida que avanzas por las carpetas, la complejidad aumenta y cada caso agrega una capacidad nueva.

### Caso A: AWS Amplify (Velocidad total)

**Objetivo**: Despliegue muy rapido. AWS resuelve hosting, SSL y CDN casi sin configuracion manual.

### Caso B: GitLab CI + S3 (Camino artesanal)

**Objetivo**: Entender los cimientos del deploy. Aprendes sobre buckets, permisos IAM y sincronizacion.

### Caso C: Terraform (Infraestructura como codigo)

**Objetivo**: Profesionalizar el despliegue. La nube se escribe en archivos versionables y repetibles.

### Caso D: Serverless Basic (Logica reactiva)

**Objetivo**: Agregar backend sin servidores permanentes. Formularios y APIs que usan Lambda y DynamoDB.

### Caso E: Persistence Pro (Modelado NoSQL real)

**Objetivo**: Subir el nivel de persistencia. Aqui ya no se trata solo de guardar datos, sino de modelarlos segun las consultas que el negocio necesita.

Que demuestra este caso:

- tabla unica en DynamoDB
- indices secundarios globales para lecturas operativas
- escritura transaccional de orden y auditoria
- consultas por cliente, estado y producto
- una landing publica que permite probar la API real

Este caso ya esta **resuelto, desplegado y validado** en AWS.

### Casos F-I: expansion de seguridad, eventos y operacion

- **F - Seguridad**: Cognito, WAF y endurecimiento de acceso.
- **G - Eventos**: Arquitectura asincrona validada con EventBridge, SQS, DLQ y una landing publica para explicar por que se desacopla el procesamiento.
- **H - Observabilidad**: CloudWatch, trazas y salud operativa.
- **I - GenAI**: Integracion de modelos de lenguaje con Bedrock.

`Caso G` ya esta **desplegado y validado** en AWS. Es importante porque muestra el paso desde
"guardar datos" a "reaccionar a hechos de negocio" sin bloquear la API de entrada.

### Caso J: Dockerizacion (Combo industrial)

**Objetivo**: Empaquetar aplicaciones para que corran igual en local y en AWS.

### Caso K: Kubernetes en AWS (Orquestacion EKS)

**Objetivo**: Gestionar flotas de contenedores con self-healing, balanceo y despliegue real en la nube.

### Caso L: FinOps (Optimizacion financiera)

**Objetivo**: Controlar costos, gobernanza y acceso para operar con madurez.

---

## Como se conecta todo

1. Haces un cambio en tu PC o entorno de desarrollo.
2. Ejecutas validaciones locales.
3. Haces `push` a GitLab.
4. El pipeline valida, construye y despliega segun el caso.
5. Revisas costos, seguridad y estado operativo antes de cerrar el ciclo.

---

## Idea clave para entender el Caso E

En SQL solemos pensar en tablas relacionadas. En DynamoDB, y especialmente en este repositorio, la pregunta cambia:

- no se parte de "que tablas necesito"
- se parte de "que consultas debe responder la aplicacion"

Por eso `Caso E` es importante: muestra un cambio de mentalidad que se espera en roles senior de backend cloud.

---

Empieza por [README.md](../README.md) y luego entra a [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md) si quieres ver un ejemplo completo de persistencia NoSQL aplicada.
