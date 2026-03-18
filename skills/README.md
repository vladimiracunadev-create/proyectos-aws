# Skills Del Monorepo

Este directorio contiene skills reutilizables para Claude Code, adaptados a los flujos de AWS y GitLab de este repositorio.

## Como invocar un skill

Desde cualquier sesion de Claude Code en este repositorio, escribe:

```
/nombre-del-skill
```

Ejemplo:

```
/docs-portal-sync
/visualizacion-evidencia caso-h
/aws-case-scaffolder caso-n-nombre
```

Claude lee el `SKILL.md` correspondiente y ejecuta el flujo documentado en el. No hace falta explicar el contexto cada vez: el skill ya lo conoce.

---

## Skills Disponibles

### `aws-case-scaffolder`
Crea un nuevo modulo `caso-*` con la estructura estandar del repositorio.
Usalo al agregar un nuevo caso de AWS o al convertir un caso proyectado en uno ejecutable.

### `gitlab-aws-pipeline-editor`
Agrega o ajusta jobs de GitLab CI para lint, seguridad, Terraform, OIDC, despliegue y publicacion de artefactos.
Usalo cuando edites `.gitlab-ci.yml`, jobs de despliegue o automatizacion por ramas.

### `docs-portal-sync`
Mantiene alineados el portal raiz, el README, la documentacion, la wiki y los enlaces de los casos.
Usalo al agregar paginas, mover archivos o corregir navegacion rota en el portal estatico.

### `terraform-aws-demo-patterns`
Aplica las convenciones de Terraform del repositorio para infraestructura demo en AWS.
Usalo al crear o actualizar codigo Terraform para S3, CloudFront, ECS, EKS, IAM o failover.

### `finops-audit-and-budgeting`
Mantiene los scripts de FinOps, los flujos de presupuestos y los dashboards de revision de costos.
Usalo al editar el caso de FinOps, scripts de auditoria AWS o automatizacion guiada por presupuesto.

### `visualizacion-evidencia`
Decide si un caso usa "Demo en Vivo" o "Reporte de Visualizacion y Resultados" segun su costo.
Para casos con recursos de costo fijo (H, J, K, M), genera el `VISUALIZATION.md` con instrucciones
paso a paso para capturar evidencia en la consola AWS antes de destruir la infraestructura.

---

## Convenciones

- Mantener el texto de los skills en ASCII salvo que un sistema externo exija caracteres no ASCII.
- Mantener `SKILL.md` enfocado en instrucciones reutilizables, no en tutoriales para usuarios finales.
- Preferir referencias a archivos existentes del repositorio en vez de duplicar explicaciones largas.
- Actualizar este indice cuando se agregue, renombre o elimine un skill.
