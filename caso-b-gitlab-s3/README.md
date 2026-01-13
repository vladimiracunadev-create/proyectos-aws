# Caso B — GitLab CI/CD → S3 (CloudFront opcional)

## Qué hace
- Cuando haces push a `main`, GitLab CI sincroniza `caso-b-gitlab-s3/` hacia tu bucket S3.
- (Opcional) Invalida CloudFront si usas CDN.

## Activación (a propósito NO está activo por defecto)
GitLab solo ejecuta pipelines si existe un archivo `.gitlab-ci.yml` en la **raíz** del repo.
Por seguridad (para no tocar otros entornos), esta plantilla está aquí dentro.

Para ACTIVAR:
1) Copia `caso-b-gitlab-s3/.gitlab-ci.yml` a la raíz del repo como `./.gitlab-ci.yml`
2) En GitLab → Settings → CI/CD → Variables crea:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - S3_BUCKET
   - (opcional) CLOUDFRONT_DISTRIBUTION_ID
3) Haz commit + push a `main`.

Testing local y validaciones
---------------------------
- Antes de activar el pipeline, prueba la sincronización localmente con AWS CLI:

```bash
# Revisa qué ocurriría sin subir nada
aws s3 sync caso-b-gitlab-s3/ s3://$S3_BUCKET/ --dryrun

# Si todo está bien, ejecuta:
aws s3 sync caso-b-gitlab-s3/ s3://$S3_BUCKET/ --delete
```

- Añade validaciones en tu pipeline (ej. comprobaciones de HTML/CSS/JS, linter) para evitar despliegues con errores.

Seguridad y permisos (IAM)
--------------------------
- Usa una política IAM con **permisos mínimos**: acceso a `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket` sobre el bucket objetivo, y `cloudfront:CreateInvalidation` si usas CloudFront.
- Para un ejemplo de política lista para usar y guía, revisa `AWS_IAM_POLICY.md` en la raíz del repo.

