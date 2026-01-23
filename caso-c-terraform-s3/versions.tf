terraform {
  required_version = ">= 1.14.0"

  backend "s3" {
    bucket = "vladimir-terraform-state-2026"
    key    = "caso-c/terraform.tfstate"
    region = "sa-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
