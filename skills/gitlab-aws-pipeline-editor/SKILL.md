---
name: gitlab-aws-pipeline-editor
description: Edit this repository's GitLab CI pipeline for AWS deployment workflows. Use when Codex needs to add or fix jobs in `.gitlab-ci.yml`, align stages, wire OIDC auth, manage Terraform plan/apply flows, publish Pages artifacts, or keep case-specific deploy logic consistent across the monorepo.
---

# GitLab AWS Pipeline Editor

Maintain `.gitlab-ci.yml` with the repository's current deployment style.

## Preserve The Existing Pipeline Shape

Keep these stage groups unless the user asks for a redesign:

- `security`
- `plan-infrastructure`
- `test`
- `deploy`

Prefer extending the current modular layout instead of replacing it.

## Match Jobs To Case Boundaries

Case-specific jobs should trigger only on relevant path changes.

Use `rules:changes` for:

- `caso-b-gitlab-s3/**/*`
- `caso-c-terraform-s3/**/*`
- `caso-l-finops-optimization/**/*`
- `caso-m-resiliencia-failover/**/*`

When adding new cases, scope rules to the new folder instead of widening existing jobs.

## Prefer OIDC Over Static Credentials

For AWS deploy jobs:

- Prefer GitLab `id_tokens`.
- Exchange the web identity token for temporary AWS credentials.
- Avoid introducing long-lived keys into job definitions.

Match the style already used by the FinOps deploy jobs unless there is a strong reason to isolate it into a helper script.

## Split Terraform Delivery Clearly

For Terraform-backed cases, keep the flow explicit:

1. `terraform init`
2. `terraform plan -out=tfplan`
3. Persist `tfplan` as an artifact
4. `terraform apply tfplan`
5. Run any post-deploy job such as CloudFront invalidation only after apply

Do not collapse plan and apply into a single hidden step if the repository already documents them separately.

## Protect Pages Publishing

The root Pages job mirrors the repository into `public/`.

When editing that job:

- Keep the portal entry files copied first.
- Keep recursive case and docs copies simple.
- Avoid destructive cleanup beyond the generated `public/` tree.
- If a new file type needs extra processing, add the smallest possible step.

## Validate Cross-File References

When pipeline jobs call local scripts or files:

- Confirm the referenced path exists in the repository.
- Keep script paths consistent with `Makefile` and case-level docs.
- Fix broken path drift immediately rather than documenting it as known debt.

## Avoid Hidden Platform Assumptions

- Remember that local development here includes PowerShell and Windows.
- If a job or helper command is shell-specific, document that constraint in the related script or markdown file.
- Prefer portable CI commands when practical.
