data "aws_caller_identity" "current" {}

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  bucket_name  = "${var.project_name}-${random_id.suffix.hex}"
  s3_origin_id = "s3-${local.bucket_name}"

  website_dir   = "${path.module}/website"
  website_files = fileset(local.website_dir, "**/*")

  ext = {
    for f in local.website_files :
    f => lower(element(split(".", f), length(split(".", f)) - 1))
  }

  mime = {
    html = "text/html; charset=utf-8"
    css  = "text/css; charset=utf-8"
    js   = "application/javascript; charset=utf-8"
    pdf  = "application/pdf"
    png  = "image/png"
    jpg  = "image/jpeg"
    jpeg = "image/jpeg"
    svg  = "image/svg+xml"
    ico  = "image/x-icon"
    txt  = "text/plain; charset=utf-8"
    json = "application/json; charset=utf-8"
  }

  # Huella del deploy: si cambia cualquier archivo en website/, esto cambia.
  deployment_id = sha1(join(",", [
    for f in local.website_files : filemd5("${local.website_dir}/${f}")
  ]))
}

# ----------------------------
# S3 (bodega privada)
# ----------------------------
#tfsec:ignore:aws-s3-enable-bucket-logging - Proyecto demo/portafolio: logging requiere bucket adicional y genera costo extra.
resource "aws_s3_bucket" "site" {
  bucket        = local.bucket_name
  force_destroy = var.force_destroy_bucket
}

resource "aws_s3_bucket_ownership_controls" "site" {
  bucket = aws_s3_bucket.site.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "site" {
  bucket = aws_s3_bucket.site.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "site" {
  bucket = aws_s3_bucket.site.id
  versioning_configuration {
    status = "Enabled"
  }
}

#tfsec:ignore:aws-s3-encryption-customer-key - Proyecto demo/portafolio: AES256 (SSE-S3) es suficiente. CMK añade costo y complejidad de KMS innecesarios aquí.
resource "aws_s3_bucket_server_side_encryption_configuration" "site" {
  bucket = aws_s3_bucket.site.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ----------------------------
# CloudFront (repartidor) + OAC
# ----------------------------
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "${var.project_name}-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

#tfsec:ignore:aws-cloudfront-enable-waf - Proyecto demo/portafolio: WAF tiene costo mínimo de ~$5/mes + reglas. No justificado para un entorno de aprendizaje.
#tfsec:ignore:aws-cloudfront-enable-logging - Proyecto demo/portafolio: logging de CloudFront requiere un bucket S3 adicional con permisos especiales.
resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  default_root_object = "index.html"
  comment             = "Caso C: Terraform + S3 privado + CloudFront (OAC)"

  origin {
    domain_name              = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id                = local.s3_origin_id
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD"]
    compress        = true

    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  #tfsec:ignore:aws-cloudfront-use-secure-tls-policy - Proyecto demo/portafolio: certificado por defecto de CloudFront. TLS personalizado requiere dominio propio + ACM.
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Policy: SOLO CloudFront puede leer el bucket
resource "aws_s3_bucket_policy" "site" {
  bucket = aws_s3_bucket.site.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontReadOnly"
        Effect    = "Allow"
        Principal = { Service = "cloudfront.amazonaws.com" }
        Action    = ["s3:GetObject"]
        Resource  = "${aws_s3_bucket.site.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn"     = aws_cloudfront_distribution.cdn.arn
            "AWS:SourceAccount" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })
}

# ----------------------------
# SUBIDA AUTOMÁTICA a S3 (esto es lo que “no veías” antes)
# ----------------------------
resource "aws_s3_object" "website" {
  for_each = { for f in local.website_files : f => f }

  bucket = aws_s3_bucket.site.id
  key    = each.key
  source = "${local.website_dir}/${each.value}"
  etag   = filemd5("${local.website_dir}/${each.value}")

  content_type = lookup(local.mime, local.ext[each.key], "application/octet-stream")

  depends_on = [aws_s3_bucket_ownership_controls.site]
}

# ----------------------------
# MARCADOR DE DEPLOY
# Cambia cuando cambia cualquier archivo en website/.
# La invalidación de CloudFront se ejecuta en el pipeline de CI
# como job separado (invalidate_cloudfront_c) usando aws-cli.
# ----------------------------
resource "aws_s3_object" "deploy_marker" {
  bucket       = aws_s3_bucket.site.id
  key          = "_deploy.txt"
  content      = local.deployment_id
  content_type = "text/plain; charset=utf-8"

  depends_on = [aws_s3_object.website]
}
