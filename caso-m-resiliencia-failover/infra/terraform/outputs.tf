# outputs.tf — Caso M: Resiliencia & Failover
# Los outputs se activan cuando los módulos correspondientes estén habilitados.
# En Fase 0 están comentados para que terraform validate pase sin errores.

# --- FASE 1: Outputs de la región primaria ---

# output "alb_primary_dns" {
#   description = "DNS del Application Load Balancer primario"
#   value       = module.alb_primary.dns_name
# }

# output "target_group_primary_arn" {
#   description = "ARN del Target Group primario (necesario para drill-failover.sh)"
#   value       = module.alb_primary.target_group_arn
# }

# output "ecs_cluster_primary" {
#   description = "Nombre del cluster ECS primario"
#   value       = module.ecs_service_primary.cluster_name
# }

# output "ecs_service_primary" {
#   description = "Nombre del servicio ECS primario"
#   value       = module.ecs_service_primary.service_name
# }

# --- FASE 2: Outputs de Route 53 y región secundaria ---

# output "api_endpoint" {
#   description = "Endpoint DNS de la API con failover configurado"
#   value       = "https://${var.api_domain}"
# }

# output "route53_health_check_id" {
#   description = "ID del Health Check de Route 53 para el ALB primario"
#   value       = var.enable_secondary_region ? module.route53_failover[0].health_check_id : "N/A"
# }

# output "alb_secondary_dns" {
#   description = "DNS del Application Load Balancer secundario (us-west-2)"
#   value       = var.enable_secondary_region ? module.alb_secondary[0].dns_name : "N/A"
# }

# --- Output de diagnóstico (siempre activo) ---

output "current_config" {
  description = "Configuración actual del despliegue (diagnóstico)"
  value = {
    primary_region           = var.primary_region
    secondary_region         = var.secondary_region
    environment              = var.environment
    app_name                 = var.app_name
    desired_count            = var.desired_count
    enable_secondary_region  = var.enable_secondary_region
    phase                    = var.enable_secondary_region ? "Fase 2 (Multi-Región)" : "Fase 0-1 (Single Region)"
  }
}
