# 🐣 Caso A: AWS Amplify (Despliegue ClickOps)

[![Nivel-0](https://img.shields.io/badge/Nivel-0_Concepto-green?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)]()

Este caso es el punto de partida del monorepo. Demuestra el método más rápido y sencillo para desplegar una aplicación moderna conectada directamente a un repositorio de Git.

---

## 🎯 Objetivo
Entender la facilidad de la **Integración Continua (CI)** nativa de AWS. El foco aquí es la velocidad de entrega y la configuración automática de certificados SSL y dominios.

## 🏗️ Arquitectura
1.  **GitLab Connection**: AWS Amplify escucha cambios en la rama `main`.
2.  **Amplify Engine**: Detecta el archivo `amplify.yml`.
3.  **Hosting Global**: Despliega el contenido en una infraestructura gestionada por Amazon que escala sola.

## 🚀 Despliegue Local (Simulación)
Puedes visualizar el sitio antes de subirlo:

```bash
# Servir estáticos localmente
npx http-server . -p 8080
```

## 💎 Características Principales
- **ClickOps**: Configuración inicial sencilla desde la consola de AWS.
- **Zero Config**: Amplify maneja el CDN (CloudFront) y S3 por ti de forma invisible.
- **Pull Request Previews**: Capacidad de ver cambios en ramas temporales antes de unirlos a `main`.

---

## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🚀 **[Guía de Instalación](../docs/INSTALL.md)**
- 🧪 **[Demo en Vivo](https://main.d1uybq9oui7h8c.amplifyapp.com/)**
