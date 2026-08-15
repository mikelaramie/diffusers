---
name: scaffold-contribution
description: >
  Scaffold a correct first Diffusers contribution from a change type and one
  in-tree reference — files, lazy imports, dummy tests, and a multi-role
  change brief. Use when adding LoRA, fixing a bug, adding tests or docs,
  scaffolding a first PR, or the user asks to start a contribution without
  reading the whole codebase.
---

# Scaffold a first contribution

Get a new engineer from a request to a correct skeleton (design + code) without
reading the whole tree. Copy **one** in-tree reference. Don't invent a new
layout.

If the ask is still a vague feature/model request (PM, researcher, paper,
checkpoint, "can we add…"), run `.cursor/skills/request-intake` first.
If the env isn't verified yet, run `.cursor/skills/dev-setup` first.

Read [reference.md](reference.md) for the change-type table and file layouts.

## 1. Classify

Pick **one** type. Confirm it with the user before writing files.

| Type | When | Next |
|---|---|---|
| New model or pipeline | New transformer/VAE/UNet or a new `DiffusionPipeline` / modular blockset | **Stop.** Use `.ai/skills/model-integration`. |
| LoRA / loader | Mixin on an existing pipeline, `from_single_file`, IP-Adapter | This skill. Reference: a neighboring mixin in `src/diffusers/loaders/lora_pipeline.py` + `tests/lora/test_lora_layers_flux.py`. |
| Scheduler | New or changed sampler | This skill. Reference: `src/diffusers/schedulers/scheduling_ddim.py` + `tests/schedulers/test_scheduler_ddim.py`. |
| Bugfix | Broken existing behavior | This skill. Edit the failing path; add/adjust the smallest test. |
| Test-only | Strengthen coverage, no prod change | This skill. Follow `.ai/testing.md`. |
| Docs | User-facing docs / docstrings only | This skill. Match `docs/source/en/` neighbors; register new pages in `_toctree.yml`. |

Default new pipelines to **modular** (see `.ai/modular.md`). That is a `model-integration` job, not this skill.

## 2. Pick one reference

Name the closest existing implementation (same modality, same loader family, same test style). Read that file and its test. Scaffold by matching it — same mixin set, same dummy-size scale, same lazy-import pattern.

If you cannot name a reference, stop and ask. Do not guess from a research repo.

## 3. Scaffold the smallest correct change

1. Work on a feature branch off up-to-date `main`. Never commit to `main`.
2. Add or edit only the files that type needs (see [reference.md](reference.md)).
3. Register new public classes in the relevant `__init__.py` lazy-import maps.
4. Tests: real classes at tiny config. No `@slow`, no `LoraTesterMixin` on an *initial model* PR. A **dedicated LoRA PR** may add `tests/lora/test_lora_layers_<model>.py` using Flux as the template.
5. Don't edit `# Copied from` blocks by hand. Don't add unused params or fallbacks.
6. Read `.ai/AGENTS.md` plus the matching guide (`.ai/models.md` / `.ai/pipelines.md` / `.ai/modular.md` / `.ai/testing.md`) for the area you touch.

Confirm the plan (type, reference path, file list) with the user, then write the skeleton.

## 4. Emit a change brief

Always end with this block (fill every section). PM, QA, and DevOps read the same artifact.

```markdown
## Change brief

- **User-facing:** what changes and why (one or two sentences)
- **Engineer:** change type, reference path, files to add/edit, tests to add
- **QA:** exact pytest commands (fast only; no `make test`)
- **DevOps / CI:** workflows this path will hit (`pr_tests` quality + consistency + fast tests if `src/` or `tests/` change; docs workflows if `docs/` change). No new CI jobs.
- **Out of scope:** what this PR is not doing
```

## 5. Hand off

| Next | Use |
|---|---|
| Vague request / gather requirements | `.cursor/skills/request-intake` |
| Finish a new model/pipeline | `.ai/skills/model-integration` |
| Strengthen tests / local CI before a PR | `.cursor/skills/pre-merge-quality` |
| Open a fork PR once READY | `.cursor/skills/ci-guardrails` |
| Review the diff before a PR | `.ai/skills/self-review` |
| Env / first clone | `.cursor/skills/dev-setup` |
