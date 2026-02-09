# 🏗️ Caso C: Terraform + CloudFront (Infraestructura como Código)

[![Nivel-2](https://img.shields.io/badge/Nivel-2_Profesionalizaci%C3%B3n-blueviolet?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)]()

Este caso de estudio representa el estándar industrial de despliegue. Aquí, la infraestructura de AWS no se crea haciendo clic, sino que se define en archivos de texto utilizando **Terraform**.

---

## 🎯 Objetivo
Eliminar el error humano mediante la **Infraestructura como Código (IaC)**. Garantizar que el entorno sea 100% reproducible y auditable, utilizando protección de estado remoto y redes de distribución global (CDN).

## 🧩 Componentes del Stack
- **Terraform**: Orquestador de la infraestructura.
- **AWS S3**: Alojamiento privado de los archivos de la web.
- **AWS CloudFront**: Red CDN con HTTPS y cache global.
- **Remote Backend**: Almacenamiento seguro del estado en la región de Ohio (`us-east-2`).

## 🛠️ Comandos de Gestión
Utiliza el Makefile central para operar este caso sin complicaciones:

```bash
make tf-init      # Conecta con el almacén de estado en la nube
make tf-plan      # Revisa qué cambios se harán en AWS
make tf-apply     # Realiza el despliegue real
make tf-security  # Audita vulnerabilidades con tfsec
```

## 🔐 Seguridad Avanzada
Este caso utiliza **Origin Access Control (OAC)**, lo que significa que el bucket de S3 es totalmente **privado**. Nadie puede entrar a S3 directamente; todo el tráfico debe pasar obligatoriamente por CloudFront.

---

## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🏗️ **[Arquitectura Detallada](../docs/ARCHITECTURE.md)**
- 🛡️ **[Seguridad IAM](../docs/IAM_SECURITY.md)**
- 🚀 **[Guía de Instalación](../docs/INSTALL.md)**
- ☁️ **[Guía Paso a Paso AWS](./AWS_PASO_A_PASO.md)**
- 🧪 **[Demos en Vivo](https://d3otfpeykrm536.cloudfront.net/)**
