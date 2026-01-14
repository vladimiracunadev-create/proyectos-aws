# Caso G: Contenedores y Microservicios (ECS) 🐳

> **Nivel 6**: Arquitectura Híbrida/Compleja

## Objetivo
Desplegar aplicaciones que no encajan en el modelo Lambda (tiempos de ejecución largos, frameworks pesados, legacy) utilizando contenedores Docker orquestados.

## Stack Tecnológico
- **Docker** (Containerización)
- **Amazon ECR** (Elastic Container Registry)
- **Amazon ECS** (Elastic Container Service - Fargate)
- **Application Load Balancer** (ALB)

## Escenario
Despliegue de una API RESTful compleja escrita en Express.js (o Python Flask) dentro de un contenedor, expuesta a través de un Load Balancer y conectada a la misma DynamoDB.

## Próximamente
Dockerfiles, Task Definitions y Servicios ECS.
