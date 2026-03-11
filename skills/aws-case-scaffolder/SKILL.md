---
name: aws-case-scaffolder
description: Create or expand a `caso-*` module that follows this monorepo's AWS case-study structure. Use when Codex needs to add a new case, promote a projected case into an implemented one, or keep case layout, naming, docs, and entry files consistent with the rest of this repository.
---

# AWS Case Scaffolder

Create new case folders with the same information architecture used across this repository.

## Build The Case Skeleton

Create only the folders that the case actually needs.

Standard baseline:

```text
caso-x-name/
|- README.md
|- AWS_PASO_A_PASO.md
|- docs/
|  |- architecture.md
```

Choose add-on folders by delivery type:

- Static site case: add `index.html`, `app.js`, `styles.css`, and `assets/`.
- Terraform case: add `main.tf`, `variables.tf`, `outputs.tf`, and `versions.tf`.
- Serverless case: add `backend/` and `frontend/`.
- Container case: add `Dockerfile`, `package.json`, server entrypoint, and `public/`.
- Kubernetes case: add `deployment.yaml`, `app/`, and `terraform/` when cluster provisioning is part of the case.
- Roadmap-first case: create docs and placeholder IaC only, and label the case clearly as projected, planned, or scaffold.

## Follow Naming Rules

- Use `caso-<letter>-<topic>` for the root folder.
- Use lowercase and hyphen-separated file or folder names unless the repository already uses a standard exception such as `README.md` or `AWS_PASO_A_PASO.md`.
- Keep case labels aligned with the root `README.md`, roadmap, and docs index.

## Update Repository References

Whenever a new case is added or promoted:

- Update `README.md`.
- Update `docs/FILE_STRUCTURE.md` if the new structure changes the repository map.
- Update portal navigation in `index.html` when the case should be reachable from the root portal.
- Update GitLab Pages copy logic only if the new files require special handling.

## Reuse Existing Patterns

Read only the closest matching case before generating a new one:

- Static hosting: `caso-a-amplify`, `caso-b-gitlab-s3`
- Terraform CDN: `caso-c-terraform-s3`
- Serverless API: `caso-d-serverless-basic`
- Containers: `caso-j-containers-ecs`
- Kubernetes: `caso-k-kubernetes-eks`
- FinOps and governance: `caso-l-finops-optimization`
- Resilience scaffolding: `caso-m-resiliencia-failover`

Copy structure and tone from the nearest case instead of inventing a new style.

## Document Status Explicitly

Every case must state one of these states in its top-level docs:

- `COMPLETADO`
- `COMPLETADO (VALIDADO)`
- `PROYECTADO`
- `FUTURO / PLANIFICADO`

When the case is not executable yet, say what is already present and what is intentionally missing.

## Keep Files Lean

- Do not create extra markdown files unless they serve navigation, architecture, deployment, or evidence.
- Prefer short placeholders over fake implementation.
- If a case is scaffold-only, leave TODO markers inside the implementation files instead of pretending the feature is finished.
