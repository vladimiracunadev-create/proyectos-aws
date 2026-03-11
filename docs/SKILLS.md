# Skills Del Monorepo

This document explains the custom Codex skills stored in `skills/` for this repository.

## Purpose

These skills package recurring repository workflows so future Codex sessions can work faster and with fewer inconsistencies.

## Current Skills

### `aws-case-scaffolder`

Use this skill to create or expand a `caso-*` module with the same layout used across the repository.

### `gitlab-aws-pipeline-editor`

Use this skill when editing `.gitlab-ci.yml`, deployment jobs, OIDC flows, or case-specific CI behavior.

### `docs-portal-sync`

Use this skill to keep `README.md`, `docs/`, `wiki/`, `index.html`, and GitLab Pages navigation aligned.

### `terraform-aws-demo-patterns`

Use this skill when creating or updating Terraform for AWS demos in this monorepo.

### `finops-audit-and-budgeting`

Use this skill for cost visibility, FinOps scripts, budget-related automation, and dashboard data generation.

## Location

The skill sources live in `skills/`:

- `skills/README.md`
- `skills/aws-case-scaffolder/SKILL.md`
- `skills/gitlab-aws-pipeline-editor/SKILL.md`
- `skills/docs-portal-sync/SKILL.md`
- `skills/terraform-aws-demo-patterns/SKILL.md`
- `skills/finops-audit-and-budgeting/SKILL.md`

## Notes

- Markdown in the skills was kept in ASCII to avoid encoding drift.
- The skills are repository-specific and intentionally reflect the AWS and GitLab patterns already present here.
