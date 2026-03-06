# variables.tf — Caso M: Resiliencia & Failover
# Todas las variables que controlan el comportamiento de los módulos.
# Editar antes de ejecutar terraform plan/apply en Fase 1+.

variable "primary_region" {
  description = "Región AWS principal donde se despliega la arquitectura Multi-AZ"
  type        = string
  default     = "us-east-1"
}

variable "secondary_region" {
  description = "Región AWS secundaria para Warm Standby (activar en Fase 2)"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Nombre del entorno (lab, staging, prod)"
  type        = string
  default     = "lab"

  validation {
    condition     = contains(["lab", "staging", "prod"], var.environment)
    error_message = "El entorno debe ser 'lab', 'staging' o 'prod'."
  }
}

variable "app_name" {
  description = "Nombre base para todos los recursos del caso"
  type        = string
  default     = "caso-m-app"
}

variable "vpc_cidr" {
  description = "CIDR block de la VPC principal"
  type        = string
  default     = "10.100.0.0/16"
}

variable "desired_count" {
  description = "Número de tasks ECS (mínimo 2 para garantizar Multi-AZ)"
  type        = number
  default     = 2

  validation {
    condition     = var.desired_count >= 2
    error_message = "desired_count debe ser >= 2 para garantizar alta disponibilidad Multi-AZ."
  }
}

variable "container_image" {
  description = "Imagen Docker a usar (Full URI: registry/imagen:tag)"
  type        = string
  default     = "public.ecr.aws/nginx/nginx:alpine"
  # Placeholder: En Fase 1 reemplazar con imagen propia del caso J o app real.
  # Ejemplo: "CUENTA.dkr.ecr.us-east-1.amazonaws.com/caso-m-app:latest"
}

variable "health_check_path" {
  description = "Path del endpoint de health check en la aplicación"
  type        = string
  default     = "/healthz"
}

variable "enable_secondary_region" {
  description = "Activar arquitectura en región secundaria (Fase 2+). Default: false"
  type        = bool
  default     = false
}

variable "route53_zone_id" {
  description = "ID de la Hosted Zone en Route 53 (requerido cuando enable_secondary_region=true)"
  type        = string
  default     = ""
  # Dejar vacío en Fase 0 y Fase 1. Completar en Fase 2.
}

variable "api_domain" {
  description = "Subdominio de la API (ej: api.tudominio.com, requerido en Fase 2)"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags adicionales a aplicar a todos los recursos"
  type        = map(string)
  default     = {}
}
