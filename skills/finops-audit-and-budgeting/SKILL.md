---
name: finops-audit-and-budgeting
description: Maintain the FinOps and cost-control workflows of this AWS monorepo. Use when Codex updates the cost dashboard, AWS resource audit scripts, budget-related automation, Cost Explorer data generation, or deployment rules intended to reduce cloud spend and surface financial risk.
---

# FinOps Audit And Budgeting

Keep cost visibility actionable and cheap to maintain.

## Main Files To Reuse

Start with these repository files:

- `generate_finops_data.py`
- `scripts/aws-resource-audit.sh`
- `scripts/aws-resource-audit.ps1`
- `caso-l-finops-optimization/`
- `docs/FINOPS_MANUAL.md`
- `.gitlab-ci.yml`
- `Makefile`

## Preserve The FinOps Loop

The repository already expresses a simple cost-control workflow:

1. inspect active resources
2. generate cost data
3. publish the dashboard
4. document actions and tradeoffs

Keep new automation aligned with that loop.

## Prefer Cheap Telemetry

- Prefer AWS APIs that are already available through the existing account setup.
- Avoid recommending new always-on observability services just to render a demo chart.
- If a feature introduces recurring cost, explain the tradeoff in the related markdown.

## Keep Output Stable

When editing generated cost data:

- keep the output path stable unless there is a strong reason to move it
- update every pipeline or deploy reference if the path changes
- avoid schema churn in `costs.json` without updating the consuming frontend

## Support Both Shell Environments

The repository already carries Bash and PowerShell audit scripts.

When changing the audit workflow:

- keep both variants aligned in covered AWS services
- preserve the `Makefile` selection logic
- document any unavoidable shell-specific behavior

## Make Risk Visible

Prefer outputs that help answer:

- what is running
- what costs money continuously
- what can be shut down now
- what should stay because it backs a documented demo

Do not turn the FinOps workflow into a raw metric dump without decision support.
