# Guía de Casos Completados

Esta guía documenta los criterios de validación, las URLs de producción y las lecciones aprendidas
de cada caso completado. Es el registro de evidencia de que los deployments están realmente vivos.

> Casos completados: **2 de 11**
> Última validación: 2026-03-22

---

## Caso 01 — AWS Amplify Hosting

### Información

| Campo | Valor |
|:---|:---|
| **Carpeta** | `caso-01-amplify-hosting/` |
| **AWS Service** | Amplify Console |
| **Completado** | Q1 2026 |
| **Región** | us-east-1 (N. Virginia) |

### URLs de producción

| Entorno | URL | Estado |
|:---|:---|:---|
| **main** | https://main.d3r1wuymolxagh.amplifyapp.com/ | ✅ Activo |
| **dev** | https://dev.d20m8tc0banvg.amplifyapp.com/ | ✅ Activo |

### Checklist de validación

- [x] Deploy automático al hacer push a `main`
- [x] Deploy automático al hacer push a `dev`
- [x] SSL activo (HTTPS) en ambas URLs
- [x] PWA instalable (Service Worker registrado)
- [x] Funciona en modo offline (caché en service-worker)
- [x] Cambio de idioma funcional (ES / EN / FR / IT / PT / ZH)
- [x] Cambio de tema funcional (dark / light)
- [x] PDFs descargables en 6 idiomas desde la UI
- [x] Static JSON API respondiendo: `/api/v1/meta.json`
- [x] `llm.txt` accesible para crawlers de LLMs
- [x] `robots.txt` y `sitemap.xml` correctos

### Cómo validar manualmente

```bash
# Verificar que el sitio responde
curl -I https://main.d3r1wuymolxagh.amplifyapp.com/

# Verificar la API estática
curl https://main.d3r1wuymolxagh.amplifyapp.com/api/v1/meta.json | python -m json.tool

# Verificar robots.txt
curl https://main.d3r1wuymolxagh.amplifyapp.com/robots.txt

# Verificar llm.txt
curl https://main.d3r1wuymolxagh.amplifyapp.com/llm.txt
```

### Lecciones aprendidas

1. **Amplify no necesita build commands** para sitios vanilla HTML/CSS/JS. El `amplify.yml` puede tener `commands: []` — Amplify sirve los archivos directamente.
2. **Multi-branch es automático**: conectar el repositorio en la consola de Amplify una sola vez, y todas las ramas nuevas se despliegan en URLs independientes.
3. **El `appRoot` en `amplify.yml`** debe apuntar a la subcarpeta exacta, no a la raíz del monorepo.
4. **Limitación clave**: sin GitHub Actions en el loop, no hay control sobre el pipeline desde GitHub (sin tests pre-deploy, sin aprobaciones).

---

## Caso 02 — S3 + GitHub Actions Deploy

### Información

| Campo | Valor |
|:---|:---|
| **Carpeta** | `caso-02-s3-github-actions/` |
| **AWS Service** | Amazon S3 |
| **Completado** | Q1 2026 |
| **Región** | us-east-2 (Ohio) |
| **Workflow** | `.github/workflows/despliegue.yml` |

### URLs de producción

| Entorno | URL | Estado |
|:---|:---|:---|
| **S3 Website** | https://mi-pagina-scrum-123.s3.us-east-2.amazonaws.com/index.html | ✅ Activo |

### Checklist de validación

- [x] Workflow se activa al hacer push a `main` con cambios en `caso-02-s3-github-actions/**`
- [x] Workflow se puede activar manualmente (`workflow_dispatch`)
- [x] El S3 bucket tiene static website hosting habilitado
- [x] `index.html` accesible públicamente
- [x] `--delete` flag funciona (archivos eliminados del repo se borran del bucket)
- [x] El workflow muestra diagnóstico de directorio (`pwd` + `ls -R`)

### Cómo verificar el último deploy

```bash
# Ver el último run del workflow
gh run list --workflow=despliegue.yml --limit=5

# Ver detalle del último run
gh run view --log $(gh run list --workflow=despliegue.yml --limit=1 --json databaseId -q '.[0].databaseId')
```

### Lecciones aprendidas

1. **`paths` filter es esencial** en monorepos: sin él, un cambio en cualquier parte del repositorio dispara todos los workflows. Con `paths: ['caso-02-s3-github-actions/**']`, solo los cambios relevantes activan este deploy.
2. **`workflow_dispatch`** es indispensable desde el inicio. Permite re-desplegar sin hacer un commit vacío.
3. **Las credenciales estáticas son el patrón de aprendizaje, no el patrón de producción.** Documentar la deuda técnica explícitamente en el README del caso es parte del aprendizaje.
4. **`--delete` puede ser peligroso** si se ejecuta sobre el bucket equivocado. Siempre verificar `AWS_REGION` y el nombre del bucket antes de un primer deploy.

### Deuda técnica documentada

| Deuda | Solución | Caso |
|:---|:---|:---|
| Credenciales estáticas (`AWS_ACCESS_KEY_ID`) | OIDC federation | Caso 03 |
| Sin CDN / HTTPS propio | CloudFront | Caso 03 |
| Sin invalidación de caché | CloudFront invalidation step | Caso 03 |
| Sin entornos separados (dev/staging/prod) | GitHub Environments | Caso 04 |

---

## Progreso acumulado

### GitHub Actions: capacidades demostradas hasta ahora

| Capacidad | Caso | Archivo |
|:---|:---|:---|
| Trigger por push a rama | 02 | `despliegue.yml` |
| `paths` filter (monorepo-aware) | 02 | `despliegue.yml` |
| `workflow_dispatch` | 02 | `despliegue.yml` |
| Secret scanning (TruffleHog) | transversal | `security-scan.yml` |
| Dependency review en PRs | transversal | `security-scan.yml` |
| Linting YAML + Markdown | transversal | `security-scan.yml` |
| Wiki sync automático | transversal | `wiki-sync.yml` |

### AWS: servicios tocados hasta ahora

| Servicio | Caso | Nivel de dominio |
|:---|:---|:---|
| Amplify Console | 01 | Deploy básico multi-branch |
| S3 (Static Hosting) | 02 | Sync básico desde Actions |
| IAM (Secrets estáticos) | 02 | ⚠️ Patrón a reemplazar con OIDC |

### Lo que viene en Caso 03

- IAM con OIDC Trust Policy
- CloudFront Distribution
- Credenciales temporales vía STS
- Invalidación de caché como step explícito
