# 🎓 Deep Dive: Ingeniería de CI/CD (OIDC & Workflows)

Este documento analiza la arquitectura de automatización que permite despliegues seguros y auditados en AWS sin el uso de secretos de larga duración.

---

## 🔐 El Flujo de Identidad: AWS OIDC

En lugar de almacenar `AWS_ACCESS_KEY_ID` en GitHub, utilizamos **OpenID Connect**.

### ¿Cómo funciona el "Handshake"?
1. **Petición de Token**: GitHub Actions solicita un token (JWT) al Identity Provider de GitHub.
2. **Intercambio**: GitHub envía este token a AWS STS (Security Token Service).
3. **Validación**: AWS verifica que el token provenga del repositorio y rama correctos (`proyectos-aws` en `main`).
4. **AssumeRole**: Si es válido, AWS entrega credenciales temporales (válidas por 1 hora) con los permisos mínimos necesarios.

**Diagrama de Confianza (IAM Policy):**
```json
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:sub": "repo:vladimiracunadev-create/proyectos-aws:ref:refs/heads/main"
  }
}
```
*Lógica: Esto garantiza que ni siquiera un fork de tu propio repo pueda desplegar en tu nube.*

---

## 🛡️ Auditoría Dinámica de Seguridad

### El Dúo: TruffleHog + Detect-Secrets

1. **TruffleHog (Análisis Forense)**:
   - Escanea el historial completo de commits (fetch-depth: 0).
   - Busca firmas conocidas de AWS, Stripe, Google, etc.
   - Es nuestra "defensa exterior" para errores pasados.

2. **Detect-Secrets (Auditoría Actual)**:
   - Compara los archivos actuales contra el `.secrets.baseline`.
   - Evita "falsos positivos" (cadenas que parecen llaves pero no lo son).
   - Es nuestra "defensa interior" para el código que está a punto de subir.

---

## 🏉 Sincronización Inteligente (`aws s3 sync`)

En `despliegue.yml`, utilizamos el flag `--delete`:
```bash
aws s3 sync ./aws-s3-scrum-mi-sitio-1 s3://mi-pagina-scrum-123 --delete
```
**Análisis de Ingeniería**:
- **Delta-only**: Solo sube los archivos que han cambiado, ahorrando ancho de banda y tiempo.
- **Clean State**: El flag `--delete` asegura que los archivos borrados en Git también se borren en S3, evitando que versiones antiguas de PDFs o scripts queden huérfanas en la web.

---

## 🏗️ Orquestación de Entornos (Branches)

| Rama | Entorno | Flujo de Build |
| :--- | :--- | :--- |
| `main` | **Producción** | Despliegue a S3 (Principal) + Amplify Production. |
| `dev` | **Staging** | Amplify Preview (URL dinámica de pruebas). |

**Lógica de Merge**: Usamos la estrategia `ort` de Git para resolver conflictos automáticamente siempre que sea posible, manteniendo la paridad de la documentación técnica en ambas ramas.

---
*La automatización es la máxima expresión de la madurez tecnológica.*
