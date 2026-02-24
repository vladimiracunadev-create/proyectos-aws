# 🏗️ Arquitectura Profunda del Sistema (FILE_ARCHITECTURE)

Este documento desglosa el "ADN" técnico del monorepo, analizando la lógica interna de los scripts de orquestación y la interconexión de sus componentes.

---

## 🧬 Anatomía del Orquestador: `hub.ps1` (PowerShell)

El `hub.ps1` no es solo un lanzador de comandos; es una capa de abstracción que gestiona la paridad entre Windows y el entorno de contenedores.

### 1. Parámetros y Utilidades (`Write-ColorOutput`)
- **Lógica**: Centraliza la salida visual para asegurar que los errores sean rojos y los éxitos verdes, mejorando la **DX (Developer Experience)**.
- **Función `Show-Help`**: Actúa como la única fuente de verdad para el uso del CLI local.

### 2. Gestión de Proyectos (`List-Projects`)
- **Lógica**: Utiliza el comando `Get-ChildItem` con un filtro `aws-*`. 
- **Profundidad**: Realiza un conteo recursivo de archivos por proyecto antes de mostrarlo, lo que da visibilidad inmediata sobre la complejidad del subproyecto detectado.

### 3. Motor de Validación (`Invoke-Validate`)
- **Check de Salud de Docker**: Antes de cualquier tarea, verifica `docker info`. Si Docker no está corriendo, aborta el proceso para evitar errores de cuelgue de PowerShell.
- **Detección Automática de Imágenes**: Si la imagen `proyectos-aws/tooling` no existe, el script decide inteligentemente:
  - Intenta usar `make tooling-build` (si `make` está instalado).
  - Si no, ejecuta un `docker build` directo apuntando a `tooling/Dockerfile.tooling`.
- **Montaje de Volumen**: Ejecuta el contenedor montando el path local como **SÓLO LECTURA** (`:ro`), protegiendo el código fuente durante las auditorías de seguridad.

---

## 🛠️ El Motor Industrial: `Makefile`

Diseñado para ser el estándar de oro en entornos Linux, macOS y WSL2.

### Comandos de "Ingeniería de Planta"
- **`tooling-validate`**: Ejecuta `/opt/tooling/scripts/validate.sh` dentro de un entorno aislado. Esto garantiza que un "Fail" en local sea idéntico a un "Fail" en GitHub Actions.
- **`k8s-demo`**: Utiliza `kind` (Kubernetes in Docker). 
  - **Lógica**: Crea el cluster, carga la imagen local (`kind load`) y aplica manifiestos de `kubectl`.
  - **Seguridad**: Aplica políticas de red (`NetworkPolicy`) y contextos de seguridad (`SecurityContext`) que son la referencia técnica de este repositorio.
- **`security-scan`**: Inyecta `detect-secrets` sobre todos los archivos, filtrando mediante el `.antigravityignore` y la lógica de pre-commit.

---

## ☁️ Configuración de Nube: `amplify.yml`

Este archivo es el contrato con **AWS Amplify Console**.

```yaml
version: 1
applications:
  - appRoot: aws-amplify-mi-sitio-1
    frontend:
      phases:
        build:
          commands: [] # No requiere build process al ser Vanilla JS
      artifacts:
        baseDirectory: . # Sirve desde la raíz del subproyecto
        files:
          - '**/*' # Incluye todos los archivos, optimizando el PWA
```
**Análisis**: Al definir `appRoot`, permitimos que Amplify ignore el resto del monorepo, optimizando los tiempos de build y reduciendo el consumo de recursos (FinOps).

---

## 📊 Catálogo de Activos Dinámicos (`assets/`)

Cada subproyecto (`aws-amplify-*` y `aws-s3-*`) mantiene una carpeta `assets/` con una arquitectura idéntica:
- **`icons/icon.svg`**: Un solo activo vectorial para generar todos los tamaños de iconos de la PWA.
- **`cv-completo.pdf` vs `cv-reducido.pdf`**: Estrategia de segmentación de información para diferentes perfiles de reclutador.
- **`LEEME_PDFS.txt`**: Documentación interna para asegurar que los PDFs estén actualizados y no sean archivos corruptos.

---

## 🔐 Archivos de Control Invisible
- **`.secrets.baseline`**: Un archivo JSON que contiene los hashes de los falsos positivos. Es la "memoria" del sistema de seguridad.
- **`.github/workflows/wiki-sync.yml`**: Un bridge que usa un token de GitHub para empujar cambios desde `docs/wiki/` al repositorio `.wiki` oculto de GitHub.

---
*Este documento es una pieza viva del ecosistema. Si modificas un script principal, actualiza su profunda explicación aquí.*
