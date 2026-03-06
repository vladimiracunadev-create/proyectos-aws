# main.tf — Caso M: Resiliencia & Failover
# Estado: SKELETON — Fase 0 (sin recursos AWS activos)
#
# Este archivo es un placeholder profesional. Descomenta y completa
# los módulos cuando inicies la Fase 1 o Fase 2.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# ============================================================
# PROVIDERS
# ============================================================

provider "aws" {
  region = var.primary_region

  default_tags {
    tags = {
      Project     = "caso-m-resiliencia"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "Vladimir Acuña"
    }
  }
}

# Provider para la región secundaria (Fase 2)
provider "aws" {
  alias  = "secondary"
  region = var.secondary_region

  default_tags {
    tags = {
      Project     = "caso-m-resiliencia"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "Vladimir Acuña"
      Role        = "secondary-region"
    }
  }
}

# ============================================================
# DATOS DE LA CUENTA
# ============================================================

data "aws_caller_identity" "current" {}

data "aws_availability_zones" "primary" {
  state = "available"
}

# ============================================================
# MÓDULOS — Descomenta cuando inicies la Fase correspondiente
# ============================================================

# --- FASE 1: Multi-AZ en región primaria ---

# module "network_primary" {
#   source = "./modules/network"
#
#   vpc_cidr           = var.vpc_cidr
#   availability_zones = slice(data.aws_availability_zones.primary.names, 0, 2)
#   environment        = var.environment
# }

# module "alb_primary" {
#   source = "./modules/alb"
#
#   name            = "${var.app_name}-primary"
#   vpc_id          = module.network_primary.vpc_id
#   public_subnets  = module.network_primary.public_subnet_ids
#   environment     = var.environment
#   health_check_path = "/healthz"
# }

# module "ecs_service_primary" {
#   source = "./modules/ecs-service"
#
#   cluster_name    = "${var.app_name}-cluster"
#   service_name    = "${var.app_name}-service"
#   desired_count   = var.desired_count
#   container_image = var.container_image
#   target_group_arn = module.alb_primary.target_group_arn
#   private_subnets  = module.network_primary.private_subnet_ids
# }

# --- FASE 2: Multi-Región + Route 53 Failover ---

# module "route53_failover" {
#   count  = var.enable_secondary_region ? 1 : 0
#   source = "./modules/route53-failover"
#
#   hosted_zone_id        = var.route53_zone_id
#   domain_name           = var.api_domain
#   primary_alb_dns       = module.alb_primary.dns_name
#   secondary_alb_dns     = module.alb_secondary[0].dns_name
#   ttl                   = 60
# }
