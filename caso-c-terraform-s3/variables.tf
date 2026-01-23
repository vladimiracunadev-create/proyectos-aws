variable "aws_region" {
  type        = string
  description = "Región donde se crea el bucket S3 (CloudFront es global)."
  default     = "us-east-2"
}

variable "project_name" {
  type        = string
  description = "Prefijo para nombrar recursos."
  default     = "caso-c-terraform-s3"
}

variable "force_destroy_bucket" {
  type        = bool
  description = "Para laboratorio: permite destruir el bucket aunque tenga objetos."
  default     = true
}
