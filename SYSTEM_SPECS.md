# 🖥️ Especificaciones del Sistema (SYSTEM_SPECS)

Este documento detalla los requerimientos físicos y lógicos necesarios para desarrollar, probar y desplegar los proyectos de este ecosistema.

---

## 💻 Requerimientos de Hardware

| Componente | Mínimo (MVP) | Recomendado (Max Tested) |
| :--- | :--- | :--- |
| **Procesador** | Dual-Core 2.0GHz | Intel Core i7-8550U (o equivalente) |
| **Memoria RAM** | 4 GB | 16 GB (DDR4) |
| **Almacenamiento** | 10 GB HDD/SSD | 50 GB SSD (NVMe recomendado) |
| **Virtualización** | Soportada en BIOS | Intel VT-x / AMD-V habilitado |

> [!NOTE]
> La virtualización es crítica para el uso fluido de **Docker Desktop** y la validación de seguridad local.

---

## 🛠️ Stack de Software (Tooling)

| Herramienta | Versión Mínima | Versión de Referencia |
| :--- | :--- | :--- |
| **Sistema Operativo** | Windows 10 / Ubuntu 20.04 | Windows 11 Home (Build 26200) |
| **Node.js** | v18.0.0 | v24.11.1 |
| **Docker** | v20.0.0 | v29.2.0 |
| **Git** | v2.30.0 | v2.53.0 |
| **AWS CLI** | v2.20.0 | v2.32.16 |
| **PowerShell** | v5.1 | v7.0+ (Sugerido para hub.ps1) |

---

## 🌐 Conectividad y Nube

- **Ancho de Banda**: Mínimo 5 Mbps para sincronización de S3 y despliegues en Amplify.
- **Acceso IAM**: Requiere permisos para gestionar S3, Amplify y Roles de IAM (OIDC).
- **DNS**: Acceso a `*.amplifyapp.com` y endpoints regionales de AWS.

---

## ✅ Matriz de Compatibilidad

| Entorno | Estado | Notas |
| :--- | :--- | :--- |
| **Windows Native** | ✅ Estable | Uso de `hub.ps1` y PowerShell. |
| **WSL2 (Ubuntu)** | ✅ Recomendado | Máxima paridad con los jobs de GitHub Actions. |
| **macOS** | ⚠️ Parcial | Requiere adaptación manual del Hub CLI a scripts `.sh`. |
| **Linux (Bare Metal)** | ✅ Estable | Uso nativo de `Makefile` y Docker. |

---
*Última actualización de especificaciones basada en auditoría de entorno v4.x.x.*
