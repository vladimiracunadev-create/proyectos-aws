data "aws_caller_identity" "current" {}

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  bucket_name  = "${var.project_name}-${random_id.suffix.hex}"
  s3_origin_id = "s3-${local.bucket_name}"

  # Carpeta local con tu sitio (el ZIP descomprimido aquí)
  website_dir   = "${path.module}/website"
  website_files = fileset(local.website_dir, "**/*")

  # Detecta extensión para content-type y cache-control
  file_ext = {
    for f in local.website_files :
    f => lower(element(split(".", f), length(split(".", f)) - 1))
  }

  mime_types = {
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

  # Cache: html corto (para ver cambios rápido), assets más largo
  cache_control = {
    for f, ext in local.file_ext :
    f => ext == "html" ? "max-age=60" :
         (ext == "css" || ext == "js") ? "max-age=3600" :
         "max-age=31536000"
  }

  # “Huella” del deploy: si cambia cualquier archivo → cambia este hash
  deployment_id = sha1(join(",", [
    for f in local.website_files : filemd5("${local.website_dir}/${f}")
  ]))
}

# 1) S3 bucket privado (bodega)
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

resource "aws_s3_bucket_server_side_encryption_configuration" "site" {
  bucket = aws_s3_bucket.site.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 2) OAC (credencial para que CloudFront lea S3 privado)
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "${var.project_name}-oac"
  description                       = "OAC for private S3 origin"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# 3) CloudFront (repartidor global)
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

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# 4) Bucket policy: SOLO esta distribución CloudFront puede leer objetos
resource "aws_s3_bucket_policy" "site" {
  bucket = aws_s3_bucket.site.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontReadOnly"
        Effect = "Allow"
        Principal = { Service = "cloudfront.amazonaws.com" }
        Action   = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.site.arn}/*"
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

# 5) Subida automática del sitio (sin aws s3 sync)
resource "aws_s3_object" "website" {
  for_each = { for f in local.website_files : f => f }

  bucket = aws_s3_bucket.site.id
  key    = each.key
  source = "${local.website_dir}/${each.value}"

  etag         = filemd5("${local.website_dir}/${each.value}")
  content_type = lookup(local.mime_types, local.file_ext[each.key], "application/octet-stream")
  cache_control = local.cache_control[each.key]

  depends_on = [aws_s3_bucket_ownership_controls.site]
}

# 6) Invalidate automático: si cambias archivos, CloudFront refresca
resource "aws_cloudfront_invalidation" "all" {
  distribution_id  = aws_cloudfront_distribution.cdn.id
  paths            = ["/*"]
  caller_reference = local.deployment_id

  depends_on = [aws_s3_object.website]
}
