# 🏗️ Arquitectura de Archivos del Sistema (FILE_ARCHITECTURE)

Este documento proporciona un análisis profundo de la estructura del monorepo, explicando el propósito y la interacción de cada archivo crítico.

---

## 📂 Mapa Genético del Monorepo

```text
proyectos-aws/
├── .github/workflows/      # 🤖 Cerebro de Automatización (CI/CD)
│   ├── despliegue.yml      # Flujo de producción para S3
│   └── security-scan.yml   # Auditoría de seguridad (SAST/Secrets)
├── aws-amplify-mi-sitio-1/ # 🌐 Proyecto A: Portfolio Amplify (PWA)
├── aws-s3-scrum-mi-sitio-1/# 🏉 Proyecto B: Portfolio S3 (Scrum focused)
├── docs/                   # 📚 Base de Conocimiento (Wiki)
├── .secrets.baseline       # 🔐 Huellas de seguridad para evitar fugas
├── Makefile                # 🛠️ Orquestador atómico (Linux/Mac/WSL2)
├── hub.ps1                 # 🛠️ Hub CLI para Windows (PowerShell)
└── amplify.yml             # ☁️ Descriptor de Build para AWS Amplify
```

---

## 🧩 Análisis de Componentes Críticos

### 1. El Orquestador Local (`hub.ps1` & `Makefile`)
- **Propósito**: Estandarizar las operaciones. Un desarrollador no necesita recordar comandos complejos de Docker o AWS; usa el Hub.
- **ADN**: El `hub.ps1` detecta el sistema operativo y delega tareas a contenedores de "tooling" para garantizar que el resultado sea idéntico en local y en la nube.

### 2. Control de Seguridad (`.secrets.baseline`)
- **Propósito**: Actúa como un "filtro de ruido". Registra qué archivos tienen contenido que *parece* un secreto pero es inofensivo, permitiendo que `detect-secrets` se enfoque en amenazas reales.

### 3. Configuración de Nube (`amplify.yml`)
- **Propósito**: Indica a AWS Amplify cómo construir y servir el subproyecto. Controla el caché, los headers de seguridad y el directorio de despliegue.

---

## 🧬 Ciclo de Vida de los Archivos

1. **Creación**: Los nuevos archivos se crean sobre la rama `dev`.
2. **Validación**: El archivo es procesado por los pre-commit hooks.
3. **Integración**: Fluye hacia `main` tras validación en PR.
4. **Despliegue**: Se transforma en activos estáticos en S3 o Amplify.

---

## 🛠️ Archivos de Soporte (Hidden Gems)

- **`NOTICE` & `LICENSE`**: Cumplimiento legal del software.
- **`amplify.yml`**: Configuración de CI/CD nativa de AWS para apps SPA.
- **`.github/workflows/wiki-sync.yml`**: Mantiene la Wiki de GitHub sincronizada con el contenido de la carpeta `docs/`.

---
*Entender la estructura es el primer paso para dominar la infraestructura.*
