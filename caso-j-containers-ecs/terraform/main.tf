# Usamos la VPC por defecto para simplificar la demo
data "aws_vpc" "default" {
  default = true
}

# Obtenemos las subnets publicas de la VPC por defecto
data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
