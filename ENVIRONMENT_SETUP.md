# 🛠️ Configuración de Entorno (ENVIRONMENT_SETUP)

Sigue esta guía para preparar tu estación de trabajo y contribuir al proyecto con el mismo estándar de calidad que el pipeline de producción.

---

## 1. Instalación de Herramientas Core

### Windows (PowerShell)
1. Instala [Node.js v24+](https://nodejs.org/).
2. Instala [Docker Desktop](https://www.docker.com/products/docker-desktop).
3. Instala [Git](https://git-scm.com/).
4. Instala [AWS CLI v2](https://aws.amazon.com/cli/).

### Linux (Ubuntu/WSL2)
```bash
sudo apt update && sudo apt install git nodejs docker.io awscli -y
```

---

## 2. Configuración de Seguridad Local

Es **obligatorio** configurar el pre-commit hook para evitar el commit accidental de secretos.

1. Instala Python 3.x.
2. Instala la herramienta:
   ```bash
   pip install pre-commit detect-secrets
   ```
3. Instala los hooks en el repositorio:
   ```bash
   pre-commit install
   ```

---

## 3. Uso del Hub CLI (Estandarización)

El Hub CLI (`hub.ps1` o `Makefile`) es tu interfaz única con el proyecto.

- **Check de Salud**: Ejecuta `.\hub.ps1 help` para verificar que el CLI responde.
- **Validación Industrial**: Ejecuta `.\hub.ps1 validate`. Esto levantará un contenedor Docker con todas las herramientas de auditoría necesarias. No necesitas instalarlas todas en tu máquina host.

---

## 4. Extensiones Recomendadas (VS Code)

Para una mejor experiencia de desarrollo (DX), instala:
- **Mermaid Editor**: Para visualizar los diagramas de arquitectura.
- **YAML**: De Red Hat, para validación de workflows.
- **Markdown All in One**: Para edición fluida de documentos.
- **GitLens**: Para trazabilidad avanzada del código.

---

## 5. Verificación Final

Ejecuta el siguiente comando para asegurar que todo está listo:
```powershell
# En Windows
./hub.ps1 list-projects

# En Linux/WSL2
make help
```

---
*Si encuentras algún problema en el setup, por favor abre un Pull Request contra este archivo.*
