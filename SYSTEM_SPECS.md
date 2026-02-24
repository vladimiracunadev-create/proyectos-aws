# 🖥️ Especificaciones Profundas del Sistema (SYSTEM_SPECS)

Este documento justifica las decisiones tecnológicas y detalla los requerimientos exactos para mantener la integridad del ecosistema `proyectos-aws`.

---

## 💻 El Rationale del Hardware

### 1. Perfil de Desarrollo Recomendado (Referencia: i7-8550U)
- **Por qué 16GB RAM?**: Docker Desktop y WSL2 consumen una media de 4GB a 8GB solo para mantener el daemon y las capas de caché de imágenes. 16GB garantizan que el IDE (VS Code) y el navegador (con múltiples pestañas de AWS) no sufran latencia.
- **Virtualización**: Se requiere soporte para **Second Level Address Translation (SLAT)** para que WSL2 funcione con el motor de utilidad de Windows.

### 2. Almacenamiento y I/O
- **IOPS**: Se recomienda SSD con al menos 500 MB/s de lectura/escritura. Las operaciones de `docker build` y `npm install` son intensivas en I/O.
- **Espacio**: 50GB dedicados permiten almacenar múltiples versiones de la imagen de `tooling` (aprox. 1.5GB cada una) y el caché de las capas de Linux.

---

## 🛠️ Matriz de Software y Justificación Técnica

| Herramienta | Versión | Justificación de Ingeniería |
| :--- | :--- | :--- |
| **Node.js** | v24.11.1 | Uso de las últimas APIs de Fetch nativo y mejoras en el motor V8 para despliegues PWA. |
| **Docker** | v29.2.0 | Soporte para `buildx` avanzado y mejoras en la gestión de volúmenes `:ro` (ReadOnly). |
| **Git** | v2.53.0 | Trazabilidad mejorada y soporte para estrategias de merge avanzadas como `ort`. |
| **AWS CLI** | v2.32.16 | Compatibilidad total con los estados de OIDC y los últimos servicios de Amplify. |

---

## 📡 Requerimientos de Red y Seguridad

### 1. Latencia y DNS
- **Resolución**: El sistema depende de la resolución rápida de `token.actions.githubusercontent.com` para la autenticación OIDC.
- **Firewall**: Deben permitirse conexiones salientes en los puertos 80, 443 (HTTPS) y 22 (SSH para Git).

### 2. Contexto de Ejecución (Windows)
- **PowerShell Execution Policy**: El script `hub.ps1` requiere `RemoteSigned` para cargar funciones externas de validación. 
- **Docker Socket**: El acceso al socket de Docker debe estar habilitado para que los scripts del Hub puedan orquestar contenedores.

---

## 🧪 Pruebas de Estrés (Benchmarks Locales)

- **Tiempo de Build Tooling**: < 180s (enRecommended Hardware).
- **Latencia de Despliegue (Sync)**: < 45s para cambios menores en archivos estáticos.
- **Arranque de K8s Demo**: < 5 min desde el comando `make k8s-demo` hasta la disponibilidad del endpoint.

---
*Este documento establece la línea base de calidad física para el software.*
