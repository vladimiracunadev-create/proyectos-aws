# Skills Del Monorepo

Este directorio contiene skills reutilizables de Codex adaptados a los flujos de AWS y GitLab usados en este repositorio.

## Skills Disponibles

### `aws-case-scaffolder`
- Crea un nuevo modulo `caso-*` con la estructura estandar del repositorio.
- Usalo al agregar un nuevo caso de AWS o al convertir un caso proyectado en uno ejecutable.

### `gitlab-aws-pipeline-editor`
- Agrega o ajusta jobs de GitLab CI para lint, seguridad, Terraform, OIDC, despliegue y publicacion de artefactos.
- Usalo cuando edites `.gitlab-ci.yml`, jobs de despliegue o automatizacion por ramas.

### `docs-portal-sync`
- Mantiene alineados el portal raiz, el README, la documentacion, la wiki y los enlaces de los casos.
- Usalo al agregar paginas, mover archivos o corregir navegacion rota en el portal estatico.

### `terraform-aws-demo-patterns`
- Aplica las convenciones de Terraform del repositorio para infraestructura demo en AWS.
- Usalo al crear o actualizar codigo Terraform para S3, CloudFront, ECS, EKS, IAM o failover.

### `finops-audit-and-budgeting`
- Mantiene los scripts de FinOps, los flujos de presupuestos y los dashboards de revision de costos del repositorio.
- Usalo al editar el caso de FinOps, scripts de auditoria AWS o automatizacion guiada por presupuesto.

## Convenciones

- Mantener el texto de los skills en ASCII salvo que un sistema externo exija caracteres no ASCII.
- Mantener `SKILL.md` enfocado en instrucciones reutilizables, no en tutoriales para usuarios finales.
- Preferir referencias a archivos existentes del repositorio en vez de duplicar explicaciones largas.
- Actualizar este indice cuando se agregue, renombre o elimine un skill.
