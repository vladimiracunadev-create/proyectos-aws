# Backend Configuration — Caso M
# Estado: LOCAL por defecto (Fase 0 — sin recursos AWS)
#
# Para Fase 1+: cambiar a backend "s3" usando el bucket de remote state
# ya configurado en el Caso C y Caso J de este repo.
#
# Ejemplo de migración a backend remoto (Fase 1+):
#
# terraform {
#   backend "s3" {
#     bucket         = "vladimir-terraform-state-CUENTA"
#     key            = "caso-m/resiliencia/terraform.tfstate"
#     region         = "us-east-1"
#     dynamodb_table = "terraform-lock"
#     encrypt        = true
#   }
# }

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
