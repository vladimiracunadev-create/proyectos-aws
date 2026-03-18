# 💻 Certificacion AWS DVA-C02 — Developer Associate

> **Cobertura actual del repositorio:** 60%
> **Costo del examen:** ~$300 USD
> **Duracion del examen:** 130 minutos, 65 preguntas
> **Validez:** 3 años
> **Recomendacion:** Segunda certificacion natural tras SAA-C03. Fuerte en Lambda y API Gateway. Requiere profundizar en CI/CD y herramientas de desarrollo.

---

## Que evalua este examen

La DVA-C02 evalua el desarrollo, despliegue y depuracion de aplicaciones en AWS. Tiene enfoque practico: espera que conozcas los SDKs, los patrones de error, los mecanismos de despliegue y la depuracion de aplicaciones serverless y en contenedores.

---

## Dominios y cobertura por caso

### Dominio 1 — Desarrollo con servicios AWS (32% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| Lambda — handler, layers, variables de entorno | Casos D, E, F, G, H | ✅ |
| API Gateway HTTP API y REST API | Casos D, E, F | ✅ |
| DynamoDB SDK — put, get, query, scan, transacciones | Caso E | ✅ |
| SQS — enviar/recibir/eliminar mensajes, visibility timeout | Caso G | ✅ |
| SNS — topics, subscripciones, fan-out | Caso G | ✅ |
| S3 SDK — upload, presigned URLs, eventos | Casos B, C | ✅ parcial |
| Cognito — tokens JWT, flujos de autenticacion | Caso F | ✅ |
| Step Functions | No cubierto | ❌ estudiar |
| AppSync y GraphQL | No cubierto | ❌ no aplica en repo |
| ElastiCache — patrones lazy loading y write-through | No cubierto | ❌ estudiar |

**Cobertura del dominio: 70%**

---

### Dominio 2 — Seguridad (26% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| IAM roles para Lambda y ECS | Todos los casos con Lambda | ✅ |
| Cognito User Pools y Identity Pools | Caso F | ✅ |
| JWT — firma, validacion, claims | Caso F (JWT Authorizer nativo) | ✅ |
| Secrets Manager en codigo (SDK) | No implementado directamente | ⚠️ |
| Parameter Store (SSM) en Lambda | No implementado | ⚠️ estudiar |
| KMS — encrypt/decrypt en SDK | No cubierto | ❌ estudiar |
| STS — AssumeRole desde codigo | Caso L (OIDC → rol) | ✅ conceptual |
| WAF — integracion con API Gateway | Caso F | ✅ |

**Cobertura del dominio: 60%**
**Gap:** Secrets Manager y SSM Parameter Store desde codigo Lambda — tema muy frecuente en el examen.

---

### Dominio 3 — Despliegue (24% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| AWS SAM — template.yaml, comandos build/deploy | Casos D, E, F, G, H | ✅ |
| CloudFormation — stacks, parametros, outputs | SAM genera CF + Caso J/K TF | ✅ |
| CodePipeline y CodeBuild | No cubierto (usamos GitLab CI) | ⚠️ conceptual |
| CodeDeploy — canary, linear, all-at-once para Lambda | No implementado | ❌ estudiar |
| ECR — build, push, pull de imagenes | Caso J y K | ✅ |
| ECS Fargate deployment | Caso J | ✅ |
| Elastic Beanstalk | No cubierto | ❌ estudiar basico |
| Blue/Green deployments | No implementado | ⚠️ estudiar |
| GitLab CI/CD como alternativa a CodePipeline | Todos los casos | ✅ practica real |

**Cobertura del dominio: 50%**
**Gap critico:** CodePipeline, CodeBuild, CodeDeploy (suite "Code*") — muy presentes en el examen aunque en la practica se use GitLab.

---

### Dominio 4 — Troubleshooting y optimizacion (18% del examen)

| Tema requerido | Cubierto por | Estado |
|---|---|---|
| CloudWatch Logs — log groups, metricas, alertas | Caso H | ✅ |
| X-Ray — trazas, service map, anotaciones | Caso H | ✅ |
| Lambda — cold start, timeout, memory tuning | Caso H (observabilidad) | ✅ |
| DynamoDB — ProvisionedThroughputExceededException | Caso E | ✅ conceptual |
| API Gateway — throttling, 429, quota | Casos D, F | ✅ parcial |
| SQS — poison pill, DLQ, visibility timeout | Caso G | ✅ |
| Lambda Powertools | Mencionado en H docs | ⚠️ no implementado |
| Distributed tracing entre servicios | No implementado (un solo servicio) | ❌ Caso O futuro |

**Cobertura del dominio: 65%**

---

## Resumen visual de cobertura

```
Dominio 1 — Desarrollo con AWS (32%):    ███████░░░  70%
Dominio 2 — Seguridad (26%):             ██████░░░░  60%
Dominio 3 — Despliegue (24%):            █████░░░░░  50%
Dominio 4 — Troubleshooting (18%):       ██████░░░░  65%

COBERTURA TOTAL ESTIMADA:                ██████░░░░  60%
```

---

## Temas criticos que NO cubre este repositorio

| Tema | Frecuencia en examen | Accion |
|---|---|---|
| CodePipeline + CodeBuild + CodeDeploy | Muy alta | Hacer 1 lab con CodePipeline basico |
| Secrets Manager desde Lambda (SDK) | Alta | Agregar a Caso F como mejora |
| SSM Parameter Store desde Lambda | Alta | Agregar a Caso D o F |
| Step Functions — state machines | Media | Lab independiente |
| ElastiCache desde codigo | Media | Lab independiente |
| Elastic Beanstalk basico | Baja-Media | Solo conceptual |
| Blue/Green con CodeDeploy para Lambda | Media | Estudiar — no implementar |
| Lambda Powertools (Tracer, Logger, Metrics) | Media | Agregar a Caso H (mejora futura) |

---

## Lo que el repositorio te da por encima del temario

El examen DVA-C02 no evalua GitLab CI/CD ni Terraform, pero el trabajo real con estas herramientas te da una comprension profunda del despliegue que los candidatos con solo teoria no tienen:

- Escribir `template.yaml` desde cero (SAM) → equivalente practico a CloudFormation
- Depurar tests de Lambda con `unittest.mock` → troubleshooting real
- Configurar JWT Authorizer nativo → comprension profunda de Cognito
- Leer X-Ray service maps en CloudWatch → troubleshooting con datos reales

---

## Que es el simulacro y donde hacerlo

El **simulacro** es un examen de practica cronometrado con preguntas similares al examen real. No es AWS oficial — son proveedores externos especializados en preparacion para certificaciones.

**Proveedores recomendados:**

| Proveedor | Formato | Costo aprox. | Por que usarlo |
|---|---|---|---|
| **Tutorials Dojo — Jon Bonso** | Practice exams online | $15-20 USD | El mas cercano al examen real. Las explicaciones de cada respuesta son muy didacticas. |
| **Stephane Maarek (Udemy)** | Curso + practice exams | $15-25 USD (con oferta) | Tiene curso especifico para DVA-C02 con mucho enfoque en SDK y CI/CD. |

**Estrategia:** hacer simulacros hasta sacar 80%+ antes de agendar el examen ($300). Los simulacros cuestan $15-20 — son la mejor inversion de preparacion.

---

## Plan de estudio recomendado

```
Semana 1:    Repasar casos D, E, F, G, H del repo — enfocarse en el SDK y los errores
Semana 2:    Hacer 1 lab completo con CodePipeline → CodeBuild → Lambda deploy
Semana 3:    Secrets Manager y SSM Parameter Store desde Lambda (2 horas practica)
Semana 4:    Step Functions — 1 state machine simple con Lambda
Semana 5:    Simulacro 1 completo (Tutorials Dojo — 65 preguntas, 130 min)
             → Repasar todos los errores con explicaciones
Semana 6:    Simulacro 2 y 3 hasta 80%+ → agendar examen
```

---

*Ultima revision: marzo 2026 — basado en guia oficial DVA-C02 de AWS Training and Certification*
