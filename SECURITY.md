# 🔐 Política de Seguridad

Este repositorio implementa un modelo de **Defensa en Profundidad** para proteger la integridad de los despliegues en la nube y evitar la fuga de credenciales.

> [!NOTE]
> Los escaneos de seguridad están configurados para reportar hallazgos sin bloquear el despliegue (`continue-on-error: true`), permitiendo visibilidad constante sin detener la agilidad de desarrollo.
> 
> **Requisito CI/CD:** Para que el escaneo de dependencias funcione, debes habilitar el **Dependency graph** en los ajustes de seguridad de tu repositorio en GitHub.

---

## 🛡️ Matriz de Herramientas de Seguridad

| Capa | Herramienta | Propósito |
| :--- | :--- | :--- |
| **Local (Hook)** | `detect-secrets` | Previene la inclusión de secretos en el historial de Git. |
| **CI (Static)** | `TruffleHog` | Escanea el repositorio en busca de secretos expuestos. |
| **Infra (OIDC)** | `GitHub OIDC` | Autenticación temporal sin llaves estáticas (Secretless CI). |
| **Infra (K8s)** | `NetPol & PSP` | Aislamiento de red y restricciones de ejecución en Kubernetes. |

---

## 🚨 Reporte de Vulnerabilidades

Si detectas un problema de seguridad:

1. **NO** abras un issue público.
2. Reporta vía **GitHub Security Advisories** o contacta directamente al responsable del repositorio.
3. Proporciona detalles claros y, si es posible, una recomendación de mitigación.

---

## 🔒 Auditoría y Cumplimiento

### Gestión de Secretos
- Usamos `.secrets.baseline` para rastrear falsos positivos y mantener un historial limpio.
- Todos los despliegues a AWS utilizan **Roles de IAM** asumidos mediante identidades federadas.

### Validación de Tooling
Ejecuta la validación de seguridad local con:
```powershell
.\hub.ps1 validate
```
Este comando ejecuta un contenedor de auditoría que verifica:
- Sintaxis YAML/Markdown.
- Presencia de secretos.
- Configuración de políticas de seguridad.

---

## ✅ Versiones Soportadas

| Versión | Estado |
| :--- | :--- |
| `main` | ✅ Soportada (Producción) |
| `dev` | 🏗️ Desarrollo (Post-validez) |

---
*Para más detalles sobre prácticas prohibidas, consulta [docs/killed.md](docs/killed.md).*
