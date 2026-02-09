# ⚡ Caso D: Serverless Basic (Lógica Distribuidora)

[![Nivel-3](https://img.shields.io/badge/Nivel-3_Arquitectura-orange?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)]()

Este caso introduce la capacidad de ejecutar código backend sin gestionar servidores, utilizando un stack 100% Serverless para manejar formularios y persistencia de datos.

---

## 🎯 Objetivo
Dominar la integración entre el frontend estático y los servicios de cómputo reactivos de AWS. Aprender a usar **AWS SAM (Serverless Application Model)** para desplegar funciones y bases de datos NoSQL de forma automatizada.

## 🏗️ Arquitectura (Stack)
- **API Gateway**: El recepcionista que expone los endpoints HTTP.
- **AWS Lambda**: El cerebro ejecutando Python/NodeJS solo cuando es necesario.
- **DynamoDB**: Almacén de datos ultra-rápido de baja latencia.
- **Amplify Hosting**: Alojamiento del frontend que consume esta API.

## 🛠️ Comandos de Gestión (Backend)
Si tienes instalado el AWS SAM CLI:

```bash
cd backend
sam build        # Prepara las funciones para la nube
sam deploy       # Despliega API + Lambda + DynamoDB
```

## 💎 Características Principales
- **Escalabilidad Infinita**: AWS levanta tantas copias como necesites.
- **Costo Cero en Reposo**: Si nadie usa el formulario, pagas $0.
- **Auto-Limpieza**: La tabla de DynamoDB está configurada con TTL para borrar registros antiguos.

---

## 🔗 Enlaces Relacionados
- ⬅️ **[Regresar al Roadmap Principal](../README.md)**
- 🏗️ **[Arquitectura Detallada](../docs/ARCHITECTURE.md)**
- 🚀 **[Guía de Instalación](../docs/INSTALL.md)**
- ☁️ **[Guía Paso a Paso AWS](./AWS_PASO_A_PASO.md)**
- 🧪 **[Demo Portafolio](https://staging.d3oq987bpa7ls7.amplifyapp.com/)** / **[API Test](https://tc78a6xibg.execute-api.us-east-2.amazonaws.com)**
