# Skills Del Monorepo

Este directorio contiene skills reutilizables para Claude Code, adaptados a los flujos de AWS y GitLab de este repositorio.

## Como invocar un skill

Desde cualquier sesion de Claude Code en este repositorio, escribe:

```
/nombre-del-skill
```

Ejemplos:

```
/sam-serverless-workflow
/caso-completion-checklist
/architecture-doc-standard
/lambda-test-patterns
/visualizacion-evidencia caso-h
/docs-portal-sync
/aws-case-scaffolder caso-n-nombre
```

Claude lee el `SKILL.md` correspondiente y ejecuta el flujo documentado. No hace falta explicar el contexto cada vez: el skill ya lo conoce.

---

## Skills Disponibles (10 total)

### Por cuando usar cada uno

| Situacion | Skill a usar |
|---|---|
| Crear un caso nuevo | `aws-case-scaffolder` |
| Hacer build/deploy/test con SAM | `sam-serverless-workflow` |
| Escribir o corregir tests de Lambda | `lambda-test-patterns` |
| Crear o revisar docs/architecture.md | `architecture-doc-standard` |
| Completar un caso (PROYECTADO → COMPLETADO) | `caso-completion-checklist` |
| Decidir Demo en Vivo vs Reporte de Evidencia | `visualizacion-evidencia` |
| Actualizar docs, portal, wiki tras cambios | `docs-portal-sync` |
| Editar .gitlab-ci.yml o pipelines | `gitlab-aws-pipeline-editor` |
| Crear o editar infraestructura Terraform | `terraform-aws-demo-patterns` |
| Trabajar con costos, FinOps, dashboards | `finops-audit-and-budgeting` |

---

## Descripcion de cada skill

### `aws-case-scaffolder`
Crea un nuevo modulo `caso-*` con la estructura estandar del repositorio.
Usalo al agregar un nuevo caso de AWS o al convertir un caso proyectado en uno ejecutable.

### `sam-serverless-workflow`
Cubre el ciclo completo de AWS SAM: build, deploy, prueba de endpoints, testing local con event files
y troubleshooting de errores frecuentes. Para casos D, E, F, G, H y futuros serverless.

### `lambda-test-patterns`
Patrones de pytest para Lambda: como mockear boto3 correctamente, cuando usar handler() vs funciones
individuales, estructura del event dict por tipo de ruta, simulacion de ClientError.
Previene los fallos de CI mas frecuentes en los casos serverless.

### `architecture-doc-standard`
Estandar obligatorio de 8 secciones y 4 diagramas Mermaid para cualquier `docs/architecture.md`.
Garantiza consistencia visual y de contenido entre todos los casos del repositorio.

### `caso-completion-checklist`
Lista ordenada de los 18 puntos a actualizar cuando un caso pasa de PROYECTADO a COMPLETADO.
Organizada en 4 bloques: archivos del caso, raiz del repo, docs/ globales, portal y wiki.
Evita el problema de "seguro faltan mas archivos".

### `visualizacion-evidencia`
Decide si un caso usa "Demo en Vivo" o "Reporte de Visualizacion y Resultados" segun su costo.
Para casos con recursos de costo fijo (H, J, K, M), genera el `VISUALIZATION.md` con instrucciones
detalladas para capturar evidencia en la consola AWS antes de destruir la infraestructura.

### `gitlab-aws-pipeline-editor`
Agrega o ajusta jobs de GitLab CI para lint, seguridad, Terraform, OIDC, despliegue y publicacion.
Usalo cuando edites `.gitlab-ci.yml`, jobs de despliegue o automatizacion por ramas.

### `docs-portal-sync`
Mantiene alineados el portal raiz, README, documentacion, wiki y enlaces de los casos.
Usalo al agregar paginas, mover archivos o corregir navegacion rota en el portal estatico.

### `terraform-aws-demo-patterns`
Aplica las convenciones de Terraform del repositorio para infraestructura demo en AWS.
Usalo al crear o actualizar codigo Terraform para S3, CloudFront, ECS, EKS, IAM o failover.

### `finops-audit-and-budgeting`
Mantiene los scripts de FinOps, flujos de presupuestos y dashboards de revision de costos.
Usalo al editar el caso de FinOps, scripts de auditoria AWS o automatizacion guiada por presupuesto.

---

## Convenciones

- Mantener el texto de los skills en ASCII salvo que un sistema externo exija caracteres no ASCII.
- Mantener `SKILL.md` enfocado en instrucciones reutilizables, no en tutoriales para usuarios finales.
- Preferir referencias a archivos existentes del repositorio en vez de duplicar explicaciones largas.
- Actualizar este indice cuando se agregue, renombre o elimine un skill.
