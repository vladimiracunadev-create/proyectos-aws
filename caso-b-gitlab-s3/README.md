# 🛠️ Caso B: S3 + GitLab CI (Automatización Básica)

[![Nivel-1](https://img.shields.io/badge/Nivel-1_Aprendizaje-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)]()

Este caso de estudio demuestra cómo automatizar la sincronización de archivos estáticos desde un repositorio a un bucket de **AWS S3** sin intervención manual, utilizando el poder de los **GitLab Runners**.

---

## 🎯 Objetivo
Aprender los fundamentos de **CI/CD** y la gestión de permisos en AWS. Este es el primer paso desde la configuración manual (Caso A) hacia la automatización profesional.

## 🏗️ Arquitectura
1.  **GitLab CI**: Detecta cambios en la carpeta `/caso-b-gitlab-s3`.
2.  **Job de Despliegue**: Inicia un contenedor con `aws-cli`.
3.  **S3 Sync**: Copia los archivos al bucket configurado, eliminando los que ya no existan.

## 🚀 Despliegue Local (Pruebas)
Si deseas replicar el despliegue desde tu máquina:

```bash
# Sincronización rápida usando el Makefile central
make deploy-b
```

*Nota: Requiere el bucket `vladimir-caso-b-site-2026` ya creado.*

## 💎 Características Principales
- **Automatización**: Cero clicks en la consola de AWS para actualizar contenido.
- **Eficiencia**: Solo sube los archivos que han cambiado realmente.
- **Seguridad**: Uso de variables de entorno para proteger las llaves de acceso.

---

## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🏗️ **[Arquitectura Detallada (Mermaid)](./docs/architecture.md)**
- 🚀 **[Guía de Instalación](../docs/INSTALL.md)**
- ☁️ **[Guía Paso a Paso AWS](./AWS_PASO_A_PASO.md)**
- 🛡️ **[Seguridad IAM](../docs/IAM_SECURITY.md)**
- 🧪 **[Demos en Vivo](http://vladimir-caso-b-site-2026.s3-website.us-east-2.amazonaws.com/)**
