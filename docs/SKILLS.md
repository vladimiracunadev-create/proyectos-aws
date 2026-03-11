# Skills Del Monorepo

Este documento describe los skills de Codex almacenados en `skills/` para este repositorio.

## Proposito

Estos skills empaquetan flujos repetidos del repositorio para que futuras sesiones de Codex trabajen mas rapido y con menos inconsistencias.

## Skills Actuales

### `aws-case-scaffolder`

Usa este skill para crear o ampliar un modulo `caso-*` con la misma estructura usada en el repositorio.

### `gitlab-aws-pipeline-editor`

Usa este skill cuando edites `.gitlab-ci.yml`, jobs de despliegue, flujos OIDC o comportamiento de CI por caso.

### `docs-portal-sync`

Usa este skill para mantener alineados `README.md`, `docs/`, `wiki/`, `index.html` y la navegacion de GitLab Pages.

### `terraform-aws-demo-patterns`

Usa este skill cuando crees o actualices Terraform para demos de AWS dentro de este monorepo.

### `finops-audit-and-budgeting`

Usa este skill para visibilidad de costos, scripts de FinOps, automatizacion relacionada con presupuestos y generacion de datos para dashboards.

## Ubicacion

Las fuentes de los skills viven en `skills/`:

- `skills/README.md`
- `skills/aws-case-scaffolder/SKILL.md`
- `skills/gitlab-aws-pipeline-editor/SKILL.md`
- `skills/docs-portal-sync/SKILL.md`
- `skills/terraform-aws-demo-patterns/SKILL.md`
- `skills/finops-audit-and-budgeting/SKILL.md`

## Notas

- El markdown de los skills se mantuvo en ASCII para evitar deriva de encoding.
- Los skills son especificos de este repositorio y reflejan intencionalmente los patrones de AWS y GitLab ya presentes aqui.
