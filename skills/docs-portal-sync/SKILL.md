---
name: docs-portal-sync
description: Keep the repository documentation and static portal in sync. Use when Codex adds, removes, or renames markdown pages, updates root navigation, fixes broken links between `README.md`, `docs/`, `wiki/`, and `index.html`, or needs to preserve the GitLab Pages browsing experience for this monorepo.
---

# Docs Portal Sync

Treat the documentation portal as a product surface, not just a file dump.

## Core Files To Check

Review these files whenever docs navigation changes:

- `README.md`
- `index.html`
- `assets/js/app.js`
- `docs/FILE_STRUCTURE.md`
- `wiki/home.md`
- `.gitlab-ci.yml` Pages job

## Keep Navigation Honest

- Do not link to files that do not exist.
- If a case is projected, link to its real `README.md` when available instead of inventing `index.html`.
- If a path changes, update both markdown links and portal hash links.

## Respect Portal Behavior

The root portal loads markdown dynamically and only intercepts relative `.md` links.

When changing docs:

- Prefer markdown targets for content intended to render inside the portal.
- Use direct HTML paths only for standalone dashboards or app entrypoints.
- Keep relative links compatible with the hash-based router.

## Preserve Pages Compatibility

The site is published as static assets through GitLab Pages.

Avoid changes that require server-side routing or build tooling unless the user explicitly wants a larger rewrite.

## Watch Encoding

- Use ASCII in markdown by default.
- If source files already contain non-ASCII text, preserve intent but avoid mixing encodings inside the same file.
- When editing a file with visible encoding corruption, prefer a focused fix instead of rewriting the entire document unless requested.

## Do A Consistency Pass

After doc edits:

1. Search for the old path or label.
2. Search for the new path or label.
3. Check the portal navigation if the file is user-facing.
4. Check the Pages copy job if the file is newly introduced.
