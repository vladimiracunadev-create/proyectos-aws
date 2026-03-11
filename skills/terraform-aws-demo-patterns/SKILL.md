---
name: terraform-aws-demo-patterns
description: Apply the AWS Terraform patterns used in this monorepo. Use when Codex creates or updates Terraform for demo-grade AWS infrastructure such as S3 plus CloudFront, ECS plus ECR, EKS, IAM, or failover scaffolds, and when it needs to preserve the repository's balance of security, cost control, and educational clarity.
---

# Terraform AWS Demo Patterns

Write Terraform that is safe, readable, and appropriate for a portfolio or training repository.

## Follow The Repository Standard

- Keep files split by role when the case is medium or large.
- Use `versions.tf` for provider and Terraform constraints.
- Use `variables.tf` for user inputs.
- Use `outputs.tf` for deployment results.
- Use `main.tf` only for small cases or the main composition layer.

## Favor Secure Defaults With Practical Exceptions

Apply secure defaults first:

- private S3 buckets
- public access blocks
- encryption at rest
- least-privilege IAM
- explicit tags

If a demo skips a production control because of cost or scope, document the reason close to the resource with a short comment. Match the current style of `tfsec` suppressions already used in the repository.

## Prefer Educational Clarity

- Name resources clearly.
- Group locals, data sources, resources, and outputs in a predictable order.
- Add short comments before non-obvious blocks.
- Avoid over-abstracting a small demo into many modules unless the repository already benefits from it.

## Keep Cost Awareness Visible

The repository is intentionally cost-sensitive.

When adding resources:

- call out anything with ongoing cost
- prefer serverless or lower-cost defaults when they still teach the concept
- document destroy paths or cleanup commands when the resource is expensive

## Align With CI Expectations

If the Terraform code is meant to run in GitLab CI:

- keep plan output names stable
- avoid interactive prompts
- make init, plan, and validate predictable from the case folder
- ensure references used by CI jobs are present and named consistently

## Case-Specific Anchors

Use the closest case as the anchor pattern:

- `caso-c-terraform-s3` for S3 plus CloudFront and object upload
- `caso-j-containers-ecs/terraform` for ECS, ALB, IAM, and ECR
- `caso-k-kubernetes-eks/terraform` for EKS cluster provisioning
- `caso-m-resiliencia-failover/infra/terraform` for staged resilience scaffolding

Read the nearest example before introducing a new layout.
