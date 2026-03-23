## Descripción

<!-- Qué hace este PR. Referencia el issue relacionado si existe: Closes #XX -->

## Tipo de cambio

- [ ] Bug fix
- [ ] Nueva feature / nuevo caso
- [ ] Mejora de documentación
- [ ] Refactor (sin cambio de funcionalidad)
- [ ] Seguridad / OIDC / IAM
- [ ] FinOps / reducción de costos

## Caso afectado

- [ ] caso-01-amplify-hosting
- [ ] caso-02-s3-github-actions
- [ ] caso-03+ (planificado)
- [ ] Transversal (CI/CD, tooling, docs)

## Checklist

### Calidad

- [ ] El código pasa los pre-commit hooks localmente (`pre-commit run --all-files`)
- [ ] No hay secretos ni credenciales en el diff
- [ ] Los workflows YAML son válidos (`yamllint`)

### Documentación

- [ ] El README del caso afectado está actualizado
- [ ] `CHANGELOG.md` refleja el cambio (si es feature o fix)
- [ ] Si se añade un caso nuevo, tiene su README con badges y tabla de certificaciones

### Seguridad

- [ ] No se añaden secrets estáticos (usar OIDC o variables de entorno)
- [ ] Los permisos IAM son mínimos necesarios
- [ ] `SECURITY.md` aplica a los cambios realizados

### Certificaciones (si aplica)

- [ ] DVA-C02: `docs/CERT_COVERAGE.md` actualizado
- [ ] SAA-C03: `docs/CERT_COVERAGE.md` actualizado
- [ ] SOA-C02: `docs/CERT_COVERAGE.md` actualizado

## FinOps (si aplica)

<!-- Costo estimado del cambio: nuevos recursos AWS, impacto en facturación -->
<!-- Si crea recursos nuevos, documéntalos en docs/FINOPS_COSTOS.md -->

## Screenshots / logs (opcional)

<!-- Captura del workflow exitoso, output de validación, etc. -->
