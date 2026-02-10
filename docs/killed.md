# ❌ KILLED: Prácticas NO Permitidas en este Repositorio

Este documento especifica explícitamente las prácticas de seguridad que **NO están permitidas** en este repositorio y proporciona alternativas seguras.

---

## 🚫 Prohibiciones Absolutas

### ❌ 1. Credenciales AWS en el Repositorio

**NO permitido:**

```bash
# ❌ NUNCA hacer esto
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtn<|EJEMPLO|>KEY
```

**Alternativa segura:**

- Usar **AWS OIDC** para GitLab CI/CD (sin credenciales de larga duración)
- Usar **GitLab CI/CD Variables** (Settings → CI/CD → Variables)
- Variables de entorno locales (nunca committear `.env`)

**Verificación:**

```bash
# Pre-commit hooks bloquearán automáticamente
git add .
git commit -m "test"
# detect-secrets DEBE fallar si hay secretos
```

---

### ❌ 2. Archivos de Estado de Terraform (.tfstate)

**NO permitido:**

```bash
# ❌ NUNCA commitear
terraform.tfstate
terraform.tfstate.backup
```

**Alternativa segura:**

- Usar **S3 Backend** con bloqueo DynamoDB
- Configurar `.gitignore` (ya incluido)

**Configuración correcta:**

```hcl
terraform {
  backend "s3" {
    bucket         = "mi-terraform-state"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

---

### ❌ 3. Secretos Hardcodeados

**NO permitido:**

```python
# ❌ NUNCA hacer esto
DATABASE_PASSWORD = "super-secret-password"
API_KEY = "sk-1234567890abcdef"
```

**Alternativa segura:**

```python
# ✅ Usar variables de entorno
import os
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
API_KEY = os.environ.get("API_KEY")
```

O usar **AWS Secrets Manager / Systems Manager Parameter Store**:

```python
import boto3
client = boto3.client('secretsmanager', region_name='us-east-1')
secret = client.get_secret_value(SecretId='my-secret')
```

---

### ❌ 4. Ejecución como Root en Contenedores

**NO permitido:**

```dockerfile
# ❌ Sin especificar usuario
FROM alpine:3.19
COPY app.py /app/
CMD ["python", "/app/app.py"]
```

**Alternativa segura:**

```dockerfile
# ✅ Usuario no-root
FROM alpine:3.19
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser
USER appuser
COPY app.py /app/
CMD ["python", "/app/app.py"]
```

---

## ✅ Prácticas Recomendadas (Alternativas Seguras)

### 1. Autenticación con OIDC (OpenID Connect)

**Para GitLab CI/CD:**

```yaml
# .gitlab-ci.yml
deploy:
  image: amazon/aws-cli:latest
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com
  before_script:
    - >
      export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s"
      $(aws sts assume-role-with-web-identity
      --role-arn ${ROLE_ARN}
      --role-session-name "GitLabRunner-${CI_PROJECT_ID}-${CI_PIPELINE_ID}"
      --web-identity-token ${GITLAB_OIDC_TOKEN}
      --duration-seconds 3600
      --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]'
      --output text))
  script:
    - aws s3 sync ./build s3://my-bucket
```

### 2. GitLab CI/CD Variables para Secretos

**Configuración:**

1. Ir a **Settings → CI/CD → Variables**
2. Agregar variables:
   - `AWS_REGION`: us-east-1
   - `ROLE_ARN`: arn:aws:iam::123456789012:role/GitLabOIDCRole
3. Marcar como "Masked" y "Protected"

### 3. AWS Systems Manager Parameter Store / Secrets Manager

```bash
# Almacenar secreto
aws secretsmanager create-secret \
  --name /myapp/database/password \
  --secret-string "my-super-secret-password"

# Recuperar en aplicación
aws secretsmanager get-secret-value \
  --secret-id /myapp/database/password \
  --query SecretString \
  --output text
```

### 4. Variables de Entorno (Localmente)

```bash
# .env (NUNCA commitear)
AWS_REGION=us-east-1
DATABASE_URL=postgresql://user:pass@localhost/db
```

```bash
# .gitignore (asegurar que está incluido)
.env
.env.*
*.env
```

---

## 🔒 Checklist de Seguridad para Contribuidores

Antes de hacer commit:

- [ ] ✅ Ejecutar `pre-commit run --all-files`
- [ ] ✅ Verificar que no hay secretos en el código
- [ ] ✅ Revisar `.gitignore` para archivos sensibles
- [ ] ✅ No commitear archivos `.tfstate`
- [ ] ✅ Usar variables de entorno para configuración
- [ ] ✅ Contenedores corren como usuario no-root
- [ ] ✅ Configuración de OIDC para CI/CD (sin keys permanentes)

---

## 📚 Referencias

- [AWS OIDC with GitLab](https://docs.gitlab.com/ee/ci/cloud_services/aws/)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)

---

## 🚨 Reporte de Incidentes

Si encuentras credenciales expuestas accidentalmente:

1. **NO** crear issue público
2. Contactar al maintainer directamente
3. Rotar credenciales inmediatamente
4. Actualizar `.secrets.baseline` si es falso positivo

---

**Última actualización:** 2026-02-09  
**Versión:** 1.0.0
