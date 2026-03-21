# Skills Del Monorepo

Este documento describe los 11 skills de Claude Code almacenados en `skills/` para este repositorio.

## Proposito

Estos skills empaquetan flujos repetidos del repositorio para que futuras sesiones de Claude Code trabajen mas rapido y con menos inconsistencias. Cada skill encapsula el conocimiento especifico del repositorio para una tarea concreta.

## Como invocar un skill

```
/nombre-del-skill [argumentos opcionales]
```

Ejemplo: `/sam-serverless-workflow`, `/visualizacion-evidencia caso-h`, `/caso-completion-checklist`

---

## Skills por categoria

### Construccion y despliegue

#### `sam-serverless-workflow`
Flujo completo de AWS SAM: build, deploy, prueba de endpoints, testing local con event files y
troubleshooting. Para casos D, E, F, G, H y cualquier caso serverless futuro.

#### `terraform-aws-demo-patterns`
Convenciones de Terraform del repositorio para infraestructura demo en AWS.
Para S3, CloudFront, ECS, EKS, IAM o failover.

### Testing

#### `lambda-test-patterns`
Patrones de pytest para Lambda: mockeo correcto de boto3, cuando usar handler() vs funciones
individuales, estructura del event dict, simulacion de errores AWS. Previene los fallos de CI
mas frecuentes en los casos serverless.

### Documentacion y arquitectura

#### `architecture-doc-standard`
Estandar obligatorio de 8 secciones y 4 diagramas Mermaid complementarios para todo
`docs/architecture.md`. Garantiza consistencia entre los 11+ casos del repositorio.

#### `caso-completion-checklist`
18 puntos ordenados en 4 bloques para promover un caso de PROYECTADO a COMPLETADO sin
dejar archivos desactualizados. Resuelve el problema del barrido incompleto.

#### `docs-portal-sync`
Sincroniza portal raiz, README, docs/, wiki/ y navegacion del GitLab Pages tras cualquier cambio.

### FinOps y evidencia

#### `visualizacion-evidencia`
Decision Demo en Vivo vs Reporte de Visualizacion segun costo del caso.
Para casos con recursos de costo fijo (H, J, K, M): genera VISUALIZATION.md detallado.

#### `finops-audit-and-budgeting`
Scripts de auditoria de costos, cuenta, creditos, Free Tier, presupuestos y dashboards de FinOps.

### Scaffolding y CI/CD

#### `aws-case-scaffolder`
Estructura estandar para crear un caso nuevo o promover uno proyectado a ejecutable.

#### `gitlab-aws-pipeline-editor`
Jobs de GitLab CI para lint, seguridad, Terraform, OIDC, despliegue y publicacion de artefactos.

### Estado y mejoras del repositorio

#### `repo-status-analysis`
Radiografia completa del repositorio: estado actual, gaps identificados, mejoras priorizadas y
proxima sesion recomendada. Se activa cuando el usuario pide explicitamente un analisis de estado,
que falta mejorar, o que es mejor para el producto. Flujo: analizar → presentar → confirmar →
generar `docs/ESTADO_Y_ROADMAP.md` → subir. Nunca guarda sin confirmacion del usuario.

---

## Tabla de decision rapida

| Situacion | Skill |
|---|---|
| Crear caso nuevo | `aws-case-scaffolder` |
| Deploy con SAM | `sam-serverless-workflow` |
| Tests fallan en CI | `lambda-test-patterns` |
| Crear architecture.md | `architecture-doc-standard` |
| Completar un caso | `caso-completion-checklist` |
| Caso con costo fijo terminado | `visualizacion-evidencia` |
| Actualizar docs y portal | `docs-portal-sync` |
| Editar .gitlab-ci.yml | `gitlab-aws-pipeline-editor` |
| Crear infra con Terraform | `terraform-aws-demo-patterns` |
| Revisar o actualizar costos | `finops-audit-and-budgeting` |
| "analiza la situacion", "que falta mejorar", "futuras mejoras" | `repo-status-analysis` |

---

## Ubicacion

```
skills/
├── README.md                          ← indice con instrucciones de uso
├── aws-case-scaffolder/SKILL.md
├── sam-serverless-workflow/SKILL.md
├── lambda-test-patterns/SKILL.md
├── architecture-doc-standard/SKILL.md
├── caso-completion-checklist/SKILL.md
├── visualizacion-evidencia/SKILL.md
├── docs-portal-sync/SKILL.md
├── gitlab-aws-pipeline-editor/SKILL.md
├── terraform-aws-demo-patterns/SKILL.md
├── finops-audit-and-budgeting/SKILL.md
└── repo-status-analysis/SKILL.md
```

## Notas

- El markdown de los skills se mantiene en ASCII para evitar deriva de encoding.
- Los skills son especificos de este repositorio y reflejan los patrones de AWS y GitLab ya presentes.
- Actualizar `skills/README.md` y este archivo al agregar, renombrar o eliminar un skill.
