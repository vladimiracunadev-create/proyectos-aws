# Manual de Aprendizaje: La Guia del Novato

Bienvenido. Si estas aqui, es porque quieres entender que hay "bajo el capo" de este proyecto. Piensa en este repositorio como un **gimnasio de arquitectura cloud**. Cada carpeta es una maquina de ejercicios distinta que te prepara para retos reales en AWS.

---

## Los fundamentos: que estamos usando

1. **Git**: Guarda el historial de todo para poder volver atras si rompemos algo.
2. **GitLab**: Aloja el codigo y ejecuta robots de `CI/CD`.
3. **AWS**: Es el terreno donde viven las apps y servicios (`S3`, `Lambda`, `CloudFront`, `DynamoDB`, `Cognito`, `CloudWatch`, `EKS`).
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

### Caso F: Security First (Identidad y perimetro)

**Objetivo**: Agregar seguridad de verdad. Gestionar quienes son los usuarios y asegurarse de que solo ellos accedan a los endpoints protegidos.

Que demuestra este caso:

- registro y login de usuarios con Cognito User Pool
- emision de tokens JWT (estandar RS256)
- validacion del token en API Gateway sin escribir codigo de criptografia
- WAF opcional como primera capa de defensa contra SQLi y XSS
- landing interactiva con flujo completo: registrar → login → perfil protegido

Este caso ya esta **completado** con tests y documentacion completa.

### Caso G: Event Driven (Arquitectura asincrona)

**Objetivo**: Aprender que no todo tiene que resolverse en la misma llamada HTTP. Publicar un hecho de negocio y dejar que otros componentes lo procesen.

Que demuestra este caso:

- EventBridge como bus de eventos
- SQS para amortiguar carga y desacoplar ritmos
- DLQ para aislar mensajes que fallan repetidamente
- SNS para notificar al final del flujo sin tocar el productor
- `/health` con doble lectura: HTML para navegador, JSON para scripts

Este caso ya esta **desplegado y validado** en AWS.

### Caso H: Observabilidad (Ver lo que no se ve)

**Objetivo**: Saber que esta pasando antes de que el usuario se queje. Medir, graficar y alertar de forma automatica.

Que demuestra este caso:

- metricas custom publicadas desde Lambda a CloudWatch
- dashboard CloudWatch definido en el SAM template (IaC — no clics en consola)
- alarmas sobre errores Lambda y latencia p99
- trazas X-Ray para seguir una peticion a traves de servicios
- la diferencia entre metricas tecnicas y metricas de negocio

Este caso ya esta **desplegado y validado** en AWS.

### Caso I: GenAI Bedrock (Inteligencia Artificial)

**Objetivo**: Integrar modelos de lenguaje de AWS en una API privada y segura.
**Estado**: proyectado — requiere el Caso F como prerequisito.

### Caso J: Dockerizacion (Combo industrial)

**Objetivo**: Empaquetar aplicaciones para que corran igual en local y en AWS.

### Caso K: Kubernetes en AWS (Orquestacion EKS)

**Objetivo**: Gestionar flotas de contenedores con self-healing, balanceo y despliegue real en la nube.

### Caso L: FinOps (Optimizacion financiera)

**Objetivo**: Controlar costos, gobernanza y acceso para operar con madurez.

### Caso M: Resiliencia y Failover

**Objetivo**: Demostrar que el sistema sobrevive a fallos de region. Alta disponibilidad y recuperacion ante desastres.
**Estado**: Fase 0 completada (scaffold, docs, IaC skeleton). Fase 1 planificada.

### Caso N: CI/CD Avanzado

**Objetivo**: Pipelines multi-stage con proteccion de entornos, aprobacion manual y rollback automatizado.
**Estado**: proyectado — requiere todos los casos anteriores como base.

### Caso O: Observabilidad Distribuida

**Objetivo**: Trazas X-Ray multi-servicio, CloudWatch Synthetics, SLOs y error budget.
**Estado**: proyectado — requiere Caso H completado y Caso M recomendado.

---

## Que significan los casos completados

Los casos ya completados no son "carpetas sueltas". Cada uno demuestra una habilidad distinta:

- **A**: publicar rapido
- **B**: automatizar un deploy basico
- **C**: definir infraestructura como codigo
- **D**: crear backend serverless
- **E**: modelar datos con criterio
- **F**: proteger endpoints con identidad y perimetro
- **G**: desacoplar procesamiento con eventos
- **H**: medir, graficar y alertar con observabilidad
- **J**: empaquetar y ejecutar contenedores
- **K**: orquestar contenedores a nivel plataforma
- **L**: gobernar costo, identidad y operacion

Si quieres una explicacion mas aterrizada de todos los casos ya terminados, revisa:

- [Guia de Casos Completados](./COMPLETED_CASES_GUIDE.md)

---

## Como se conecta todo

1. Haces un cambio en tu PC o entorno de desarrollo.
2. Ejecutas validaciones locales (`make test`, `make lint`).
3. Haces `push` a GitLab.
4. El pipeline valida (seguridad, lint, tests unitarios por caso) y despliega.
5. Revisas costos, seguridad y estado operativo antes de cerrar el ciclo.

---

## Idea clave para entender el Caso E

En SQL solemos pensar en tablas relacionadas. En DynamoDB, y especialmente en este repositorio, la pregunta cambia:

- no se parte de "que tablas necesito"
- se parte de "que consultas debe responder la aplicacion"

Por eso `Caso E` es importante: muestra un cambio de mentalidad que se espera en roles senior de backend cloud.

---

## Idea clave para entender el Caso F

En sistemas simples, el token JWT lo valida el codigo de la Lambda: importas `PyJWT`, verificas la firma, manejas errores criptograficos.

En `Caso F` cambia la idea:

- API Gateway valida el token antes de invocar la Lambda
- si el token es invalido, la Lambda nunca se llama
- la Lambda solo lee los claims que ya estan validados en `requestContext`

Eso significa que si el token es incorrecto o expirado, el costo es cero: no hay Lambda que arranque.

---

## Idea clave para entender el Caso G

En un sistema simple, una API recibe una peticion y trata de hacer todo al mismo tiempo.
Eso puede volver lenta o fragil la entrada.

En `Caso G` cambia la idea:

- la API acepta un hecho de negocio
- publica un evento
- otros componentes lo procesan despues

Eso permite:

- responder rapido
- tolerar mejor picos
- separar responsabilidades
- manejar errores sin romper al cliente

`/health` en este caso tambien tiene dos lecturas:

- para maquinas: JSON tecnico
- para personas en navegador: pagina HTML explicativa

Eso ayuda a no confundir "la API esta viva" con "todo el flujo ya se proceso".

---

## Idea clave para entender el Caso H

Una alarma que configuras a mano en la consola AWS no existe en el repositorio. Si alguien borra el stack, la alarma desaparece y nadie lo sabe.

En `Caso H` cambia la idea:

- el dashboard CloudWatch esta en el SAM template
- las alarmas estan en el SAM template
- cuando haces `sam deploy`, todo el monitoreo se crea automaticamente
- cuando haces `sam delete`, todo se destruye limpiamente

Eso es **observabilidad como codigo**: el monitoreo vive donde vive la infraestructura.

---

Empieza por [README.md](../README.md) y luego entra a [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md) si quieres ver un ejemplo completo de persistencia NoSQL aplicada.
