# 🚀 Guía de Instalación y Despliegue

Este documento explica cómo poner en marcha el proyecto en diferentes escenarios.

---

## 📂 Escenario 1: Uso con DevContainers (Recomendado)
*Ideal para desarrolladores que quieren evitar instalaciones locales.*

1.  Asegúrate de tener **Docker** y **VS Code** instalados.
2.  Instala la extensión **Remote - Containers** en VS Code.
3.  Al abrir la carpeta del proyecto, VS Code detectará el entorno y te preguntará: *"Reopen in Container"*. Haz clic ahí.
4.  ¡Listo! Ya tienes todas las herramientas instaladas dentro del contenedor.

## 📂 Escenario 2: Instalación Manual
*Para quienes prefieren gestionar sus herramientas directamente.*

### 🛠️ Requisitos Previos
Consulta [TECHNICAL_SPECS.md](./TECHNICAL_SPECS.md) para ver las versiones exactas.

###  pasos:
1.  **Clonar el repo**:
    ```bash
    git clone https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab.git
    cd proyectos-aws-gitlab
    ```
2.  **Instalar dependencias**:
    ```bash
    make install
    ```
3.  **Configurar AWS**:
    ```bash
    aws configure
    ```
4.  **Ejecutar Calidad**:
    ```bash
    make lint
    ```

## 📂 Escenario 3: Despliegue Automatizado (CI/CD)
El proyecto se despliega automáticamente en GitLab cuando haces un `push` a la rama `main`.

1.  Configura tus **Variables CI/CD** en GitLab:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `S3_BUCKET` (Para el Caso B)
2.  Sube tus cambios:
    ```bash
    git add .
    git commit -m "feat: nuevo componente"
    git push origin main
    ```
