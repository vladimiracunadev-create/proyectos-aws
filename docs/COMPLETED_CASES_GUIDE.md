# Guia de Casos Completados

Este documento explica, en lenguaje simple, que demuestra cada caso que ya esta
`COMPLETADO` o `COMPLETADO (VALIDADO)` dentro del monorepo y como leerlos sin perderse.

---

## Para que sirve esta guia

No todos los casos se entienden igual de rapido.

- algunos muestran hosting y despliegue
- otros muestran backend y datos
- otros muestran integracion asincrona
- otros muestran contenedores, Kubernetes o FinOps

La idea aqui es responder cuatro preguntas para cada caso:

1. que se hizo
2. por que se hizo asi
3. que problema resuelve
4. que deberias mirar primero

---

## Caso A - Amplify

**Que se hizo**

Se publico un frontend usando AWS Amplify conectado al repositorio.

**Por que**

Porque es la forma mas rapida de sacar una web a internet sin administrar infraestructura compleja.

**Que resuelve**

- hosting
- SSL
- CDN
- deploy rapido por rama

**Que mirar primero**

- [README raiz](../README.md)
- [Caso A](../caso-a-amplify/README.md)

---

## Caso B - S3 + GitLab CI

**Que se hizo**

Se despliega un sitio estatico a S3 usando pipeline y AWS CLI.

**Por que**

Para entender que pasa debajo de una solucion mas automatizada como Amplify.

**Que resuelve**

- automatizacion basica de deploy
- uso de AWS CLI
- comprension de permisos y buckets

**Que mirar primero**

- [Caso B](../caso-b-gitlab-s3/README.md)
- [Paso a paso Caso B](../caso-b-gitlab-s3/AWS_PASO_A_PASO.md)

---

## Caso C - Terraform + CloudFront

**Que se hizo**

La infraestructura se definio como codigo con Terraform y se aseguro la entrega mediante CloudFront.

**Por que**

Porque desplegar con consola no escala bien cuando se necesita repetir, auditar y versionar cambios.

**Que resuelve**

- reproducibilidad
- control de cambios
- mejor seguridad de origen
- CDN global

**Que mirar primero**

- [Caso C](../caso-c-terraform-s3/README.md)
- [Arquitectura Caso C](../caso-c-terraform-s3/docs/architecture.md)

---

## Caso D - Serverless Basic

**Que se hizo**

Se construyo una API serverless con API Gateway, Lambda y DynamoDB.

**Por que**

Porque no siempre conviene tener servidores activos todo el tiempo para una carga intermitente.

**Que resuelve**

- backend bajo demanda
- menos administracion de servidores
- integracion simple con servicios administrados

**Que mirar primero**

- [Caso D](../caso-d-serverless-basic/README.md)
- [Paso a paso Caso D](../caso-d-serverless-basic/AWS_PASO_A_PASO.md)

---

## Caso E - Persistence Pro

**Que se hizo**

Se diseno una API con DynamoDB usando Single Table Design, GSIs y auditoria transaccional.

**Por que**

Porque DynamoDB no se modela como SQL tradicional; se modela segun las consultas del negocio.

**Que resuelve**

- lecturas por patron de acceso
- trazabilidad de eventos de negocio
- persistencia eficiente sin scans innecesarios

**Que mirar primero**

- [Caso E](../caso-e-dynamodb-persistence/README.md)
- [Arquitectura Caso E](../caso-e-dynamodb-persistence/docs/architecture.md)

---

## Caso F - Security First (Cognito + JWT + WAF)

**Que se hizo**

Se implemento un modelo de seguridad perimetral con un DEMO principal en HTTP API + JWT Authorizer y una pagina WAF auxiliar separada para demostrar el perimetro sin confundir el producto.

**Por que**

Porque ningun sistema de produccion deberia exponer endpoints sin autenticacion. Y la validacion del token no deberia vivir en el codigo de la Lambda sino en la infraestructura.

**Que resuelve**

- gestion de identidades (registro, login, tokens JWT)
- autorizacion sin codigo de criptografia en Lambda
- proteccion contra SQLi y XSS antes del API (pagina WAF auxiliar)
- prerequisito directo para el Caso I (GenAI expuesto publicamente)

**Que mirar primero**

- [Caso F](../caso-f-security-cognito/README.md)
- [Arquitectura Caso F](../caso-f-security-cognito/docs/architecture.md)
- [Paso a paso Caso F](../caso-f-security-cognito/AWS_PASO_A_PASO.md)
- [Visualization Caso F](../caso-f-security-cognito/VISUALIZATION.md)

**Como funciona el JWT sin codigo**

En DEMO, el JWT Authorizer de API Gateway HTTP API valida la firma RS256, el issuer y el audience de Cognito antes de llamar a la Lambda. La pagina WAF auxiliar existe para mostrar el perimetro en un despliegue separado y enlazado. La Lambda no valida criptografia manual.

---

## Caso G - Event Driven

**Que se hizo**

Se desplego una arquitectura asincrona con:

- API Gateway
- Lambda publicadora
- EventBridge
- SQS
- DLQ
- Lambda consumidora
- SNS

Ademas, la API publica:

- una landing principal en `/`
- un endpoint `/health` amigable para navegador
- salida JSON para herramientas cuando pides `?format=json`

**Por que**

Porque una API no deberia intentar hacer todo en la misma llamada si eso vuelve lenta o fragil la entrada.

**Que resuelve**

- desacoplamiento entre productor y consumidor
- absorcion de picos con cola
- reintentos sin romper la peticion original
- aislamiento de errores con DLQ
- base para observabilidad futura

**Que mirar primero**

- [Caso G](../caso-g-event-driven/README.md)
- [Arquitectura Caso G](../caso-g-event-driven/docs/architecture.md)
- [Paso a paso Caso G](../caso-g-event-driven/AWS_PASO_A_PASO.md)

**Como leer `/health`**

- en navegador: explica para que existe el chequeo
- en scripts o monitoreo: devuelve JSON tecnico
- importante: confirma que la puerta de entrada esta viva, pero no prueba por si sola todo el flujo asincrono

---

## Caso H - Observabilidad (CloudWatch + X-Ray)

**Que se hizo**

Se implemento observabilidad completa como codigo: dashboard CloudWatch definido en el SAM template, alarmas sobre errores Lambda y latencia p99, metricas custom desde Lambda y trazas X-Ray.

**Por que**

Porque no saber que falla hasta que el usuario se queja es una postura reactiva. La observabilidad como codigo permite que el monitoreo nazca y muera con la infraestructura, sin configuracion manual.

**Que resuelve**

- metricas custom de negocio publicadas desde Lambda
- dashboard CloudWatch definido en IaC (no en consola)
- alarmas sobre errores Lambda y latencia p99
- trazas distribuidas X-Ray sin codigo adicional

**Que mirar primero**

- [Caso H](../caso-h-observability/README.md)
- [Arquitectura Caso H](../caso-h-observability/docs/architecture.md)
- [Paso a paso Caso H](../caso-h-observability/AWS_PASO_A_PASO.md)
- [Reporte de Visualizacion Caso H](../caso-h-observability/VISUALIZATION.md)

**Como leer la evidencia**

Este caso no se deja publicado de forma permanente porque el dashboard CloudWatch tiene costo fijo. La referencia principal para evaluarlo es el reporte de visualizacion, que documenta:

- estados de la landing por ventana
- dashboard dividido en dos mitades por tamano
- trazas X-Ray
- procedimiento de eliminacion segura sin tocar otros casos

---

## Caso J - Docker + ECS

**Que se hizo**

La aplicacion se empaqueto en Docker y se ejecuto en ECS Fargate.

**Por que**

Porque a veces necesitas procesos mas durables o portables que una Lambda.

**Que resuelve**

- empaquetado consistente
- portabilidad
- ejecucion administrada de contenedores

**Que mirar primero**

- [Caso J](../caso-j-containers-ecs/README.md)
- [Arquitectura Caso J](../caso-j-containers-ecs/docs/architecture.md)

---

## Caso K - Kubernetes en EKS

**Que se hizo**

Se desplego un cluster EKS con aplicacion real y balanceo.

**Por que**

Porque Kubernetes aparece cuando necesitas un nivel mayor de orquestacion o ya trabajas en un ecosistema que lo exige.

**Que resuelve**

- orquestacion de contenedores
- self-healing
- despliegues a nivel cluster

**Que mirar primero**

- [Caso K](../caso-k-kubernetes-eks/README.md)
- [Arquitectura Caso K](../caso-k-kubernetes-eks/docs/architecture.md)

---

## Caso L - FinOps & Governance

**Que se hizo**

Se agregaron controles de costo, gobernanza e identidad con Budgets, OIDC e IAM.

**Por que**

Porque cloud maduro no es solo desplegar: tambien es controlar acceso, riesgo y gasto.

**Que resuelve**

- costos visibles
- menor dependencia de credenciales permanentes
- mejor postura de seguridad y operacion

**Que mirar primero**

- [Caso L](../caso-l-finops-optimization/README.md)
- [Arquitectura Caso L](../caso-l-finops-optimization/docs/architecture.md)

---

## Orden recomendado para entender el monorepo

1. [README.md](../README.md)
2. [BEGINNERS_GUIDE.md](./BEGINNERS_GUIDE.md)
3. [ARCHITECTURE.md](./ARCHITECTURE.md)
4. [caso-e-dynamodb-persistence/README.md](../caso-e-dynamodb-persistence/README.md)
5. [caso-f-security-cognito/README.md](../caso-f-security-cognito/README.md)
6. [caso-g-event-driven/README.md](../caso-g-event-driven/README.md)
7. [caso-h-observability/README.md](../caso-h-observability/README.md)
8. [caso-j-containers-ecs/README.md](../caso-j-containers-ecs/README.md)
9. [caso-k-kubernetes-eks/README.md](../caso-k-kubernetes-eks/README.md)
10. [caso-l-finops-optimization/README.md](../caso-l-finops-optimization/README.md)

---

_Ultima actualizacion: 2026-03-18_
