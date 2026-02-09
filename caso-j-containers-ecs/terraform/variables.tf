variable "aws_region" {
  description = "AWS Region to deploy resources"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "vladimir-case-j"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
