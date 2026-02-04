# ❌ KILLED: Prácticas NO Permitidas en este Repositorio

Este documento especifica explícitamente las prácticas de seguridad que **NO están permitidas** en este repositorio y proporciona alternativas seguras.

---

## 🚫 Prohibiciones Absolutas

### ❌ 1. Credenciales AWS en el Repositorio

**NO PERMITIDO:**

- Archivos `.aws/credentials`
- Variables `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` hardcodeadas
- Archivos `.env` con credenciales AWS
- Claves IAM en código fuente
- Tokens de sesión en commits

**RAZÓN:** Las credenciales comprometidas pueden resultar en:
- Acceso no autorizado a recursos AWS
- Costos inesperados por uso malicioso
- Violaciones de datos
- Compromiso de la cuenta AWS

---

### ❌ 2. Archivos de Estado de Terraform (.tfstate)

**NO PERMITIDO:**
- `*.tfstate`
- `*.tfstate.backup`
- Cualquier archivo de estado de Terraform en Git

**RAZÓN:**
- Los archivos `.tfstate` contienen información sensible (IPs, IDs de recursos, outputs)
- Pueden contener secretos en texto plano
- Son archivos grandes que no deben versionarse

**ALTERNATIVA:**
- Usar backend remoto (S3 + DynamoDB para locking)
- Configurar `.gitignore` apropiadamente (✅ ya configurado)

---

### ❌ 3. Secretos Hardcodeados

**NO PERMITIDO:**
- API keys en código
- Passwords en archivos de configuración
- Tokens de acceso en scripts
- Certificados privados (`.pem`, `.key`, `.p12`)

**RAZÓN:**
- Exposición pública en GitHub
- Difícil rotación de secretos
- Violación de principios de seguridad

---

### ❌ 4. Ejecución como Root en Contenedores

**NO PERMITIDO:**
- Contenedores Docker que corren como `root`
- Imágenes sin `USER` no-root especificado
- Pods de Kubernetes sin `securityContext`

**RAZÓN:**
- Principio de mínimo privilegio
- Reducción de superficie de ataque
- Prevención de escalación de privilegios

**ALTERNATIVA:**
- ✅ Usar `USER` no-root en Dockerfile (ver `tooling/Dockerfile.tooling`)
- ✅ Configurar `securityContext` en Kubernetes (ver `k8s/tooling-job/job.yaml`)

---

## ✅ Prácticas Recomendadas (Alternativas Seguras)

### 1. Autenticación con OIDC (OpenID Connect)

**Para GitHub Actions → AWS:**

```yaml
# .github/workflows/deploy.yml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
```

**Ventajas:**
- ✅ Sin credenciales de larga duración
- ✅ Tokens temporales automáticos
- ✅ Auditoría completa en CloudTrail
- ✅ Permisos granulares por repositorio/rama

**Configuración en AWS:**
1. Crear Identity Provider OIDC en IAM
2. Crear rol IAM con trust policy para GitHub
3. Asignar permisos mínimos necesarios

---

### 2. GitHub Secrets para Variables Sensibles

**Para valores que no pueden ser públicos:**

```yaml
# .github/workflows/example.yml
env:
  API_KEY: ${{ secrets.API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**Configuración:**
1. Ir a Settings → Secrets and variables → Actions
2. Agregar secrets necesarios
3. Referenciar con `${{ secrets.SECRET_NAME }}`

---

### 3. AWS Systems Manager Parameter Store / Secrets Manager

**Para secretos en runtime:**

```bash
# Obtener secreto en tiempo de ejecución
aws ssm get-parameter --name /app/database/password --with-decryption
aws secretsmanager get-secret-value --secret-id prod/db/password
```

**Ventajas:**
- ✅ Rotación automática de secretos
- ✅ Encriptación en reposo (KMS)
- ✅ Auditoría de accesos
- ✅ Versionado de secretos

---

### 4. Variables de Entorno (Localmente)

**Para desarrollo local:**

```bash
# .env (NUNCA commitear)
AWS_PROFILE=dev-profile
AWS_REGION=us-east-1

# Usar AWS CLI con profiles
aws configure --profile dev-profile
export AWS_PROFILE=dev-profile
```

**Asegurar con `.gitignore`:**
```gitignore
.env
.env.*
!.env.example
```

---

## 🔒 Checklist de Seguridad para Contribuidores

Antes de hacer commit, verifica:

- [ ] No hay credenciales AWS en el código
- [ ] No hay archivos `.tfstate` en el commit
- [ ] No hay secretos hardcodeados
- [ ] Los archivos `.env` están en `.gitignore`
- [ ] Pre-commit hooks están instalados (`pre-commit install`)
- [ ] `detect-secrets` no reporta alertas
- [ ] Contenedores Docker usan usuario no-root
- [ ] Manifiestos K8s tienen `securityContext`

---

## 📚 Referencias

- [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GitHub OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Terraform Backend Configuration](https://developer.hashicorp.com/terraform/language/settings/backends/s3)

---

## 🚨 Reporte de Incidentes

Si encuentras credenciales expuestas en este repositorio:

1. **NO** las uses ni las compartas
2. Reporta inmediatamente a través de GitHub Security Advisories
3. Contacta al maintainer del repositorio
4. Las credenciales serán rotadas inmediatamente

---

**Última actualización:** 2026-02-04  
**Mantenido por:** Equipo de Seguridad - proyectos-aws
