# Skills For This Monorepo

This directory contains reusable Codex skills tailored to the AWS and GitLab workflows used in this repository.

## Available Skills

### `aws-case-scaffolder`
- Create a new `caso-*` module with the repository's standard folder layout.
- Use when adding a new AWS case study or promoting a projected case into an executable one.

### `gitlab-aws-pipeline-editor`
- Add or adjust GitLab CI jobs for lint, security, Terraform, OIDC, deploy, and artifact publishing.
- Use when editing `.gitlab-ci.yml`, deployment jobs, or branch-based automation.

### `docs-portal-sync`
- Keep the root portal, README, docs, wiki, and case links aligned.
- Use when adding pages, moving files, or fixing broken navigation in the static portal.

### `terraform-aws-demo-patterns`
- Apply the repository's Terraform conventions for AWS demo infrastructure.
- Use when creating or updating S3, CloudFront, ECS, EKS, IAM, or failover Terraform code.

### `finops-audit-and-budgeting`
- Maintain the repository's FinOps scripts, budgeting workflows, and cost review dashboards.
- Use when editing the FinOps case, AWS audit scripts, or budget-driven deployment automation.

## Conventions

- Keep skill text in ASCII unless a non-ASCII character is required by an external system.
- Keep `SKILL.md` focused on reusable instructions, not end-user tutorials.
- Prefer references to existing repository files over duplicating long explanations.
- Update this index when a skill is added, renamed, or removed.
