---
name: scaffold-contribution
description: >
  Scaffold a correct Diffusers contribution from a change type and one
  in-tree reference — files, lazy imports, tests, and a multi-role change
  brief. Use when adding a scheduler, community pipeline, training example,
  LoRA mixin, docs, tests, or a bugfix; scaffolding a first PR; or the
  user asks to start a contribution without reading the whole codebase.
---

# Scaffold a contribution

Get from a classified request to a correct skeleton without reading the
whole tree. Copy **one** in-tree reference. Don't invent a new layout.

If the ask is still vague (PM, researcher, paper, checkpoint, "can we
add…"), run `.cursor/skills/request-intake` first.
If the env isn't verified yet, run `.cursor/skills/dev-setup` first.

Read [reference.md](reference.md) for the change-type table and file layouts.
Handbook: `docs/source/en/conceptual/contribution.md`.
Philosophy (models / pipelines / schedulers):
`docs/source/en/conceptual/philosophy.md`.

PRs from this kit go to **this fork's** `main` (`mikelaramie/diffusers`).
The user is the maintainer — confirming the plan **is** the ack.

## 1. Classify

Pick **one** type. Confirm it with the user before writing files.

| Type | When | Next |
|---|---|---|
| New model or pipeline | New transformer/VAE/UNet or a new `DiffusionPipeline` / modular blockset | **Stop.** Read philosophy, then `.ai/skills/model-integration`. |
| Scheduler | New or changed sampler | This skill. **Read philosophy first.** Reference: `scheduling_ddim.py` + `test_scheduler_ddim.py`. |
| Community pipeline | Experimental / one-off inference, not a new core architecture | This skill. Single file under `examples/community/`. Tutorial: `one_step_unet.py`. |
| Official training example | Maintained how-to under `examples/` (not `community` / `research_projects`) | This skill. Neighbor: `examples/dreambooth/`. |
| Research training example | Experimental training under `examples/research_projects/` | This skill. Author-maintained; no test required. |
| LoRA / loader | Mixin on an **existing** pipeline (`from_single_file`, IP-Adapter, …) | This skill. Neighbor mixin in `src/diffusers/loaders/lora_pipeline.py`. |
| Bugfix | Broken existing behavior, including good first/second issues | This skill. Edit the failing path; add/adjust the smallest test. |
| Test-only | Strengthen coverage, no prod change | This skill. Follow `.ai/testing.md`. |
| Docs | User-facing docs / docstrings / translation | This skill. Match `docs/source/<lang>/` neighbors; register new pages in `_toctree.yml`. |
| Hub custom block | Package a `ModularPipelineBlocks` subclass for the Hub | **Stop.** `.ai/skills/custom-blocks`. |
| CLI run / schema | Generate or inspect a pipeline from the terminal | **Stop.** `.ai/skills/diffusers-cli`. |

Default **new** pipelines to **modular** (`.ai/modular.md`). That is a
`model-integration` job, not this skill. Do not put a new SOTA architecture
in `examples/community` to dodge philosophy.

## 2. Pick one reference

Name the closest existing implementation (same modality, same loader family,
same test style, same example folder). Read that file and its test (or
README). Scaffold by matching it.

If you cannot name a reference, stop and ask. Do not guess from a research
repo unless `model-integration` is in use and the user pointed at it.

## 3. Scaffold the smallest correct change

1. Work on a feature branch off up-to-date `main`. Never commit to `main`.
2. Add or edit only the files that type needs (see [reference.md](reference.md)).
3. Register new **public library** classes in the relevant `__init__.py`
   lazy-import maps. Community pipelines and training scripts are not
   lazy-imported from `src/diffusers`.
4. Tests: real classes at tiny config. No `@slow` / `LoraTesterMixin` on an
   *initial model* PR. Official examples need a `test_*.py` in the example
   folder; research examples and community pipelines do not.
5. Don't edit `# Copied from` blocks by hand. Don't add unused params or fallbacks.
6. Read `.ai/AGENTS.md` plus the matching guide for the area you touch
   (`.ai/models.md` / `.ai/pipelines.md` / `.ai/modular.md` / `.ai/testing.md`).
   Schedulers: philosophy + a neighboring `scheduling_*.py`.

Confirm the plan (type, reference path, file list) with the user, then write
the skeleton.

## 4. Emit a change brief

Always end with this block (fill every section). PM, QA, and DevOps read
the same artifact.

```markdown
## Change brief

- **User-facing:** what changes and why (one or two sentences)
- **Engineer:** change type, reference path, files to add/edit, tests to add
- **QA:** exact pytest commands (fast only; no `make test`)
- **DevOps / CI:** workflows this path will hit (`pr_tests` quality + consistency + fast tests if `src/`, `tests/`, or `examples/**/*.py` change; docs workflows if `docs/` change). No new CI jobs.
- **Out of scope:** what this PR is not doing
```

## 5. Hand off

| Next | Use |
|---|---|
| Vague request / gather requirements | `.cursor/skills/request-intake` |
| Finish a new model/pipeline | `.ai/skills/model-integration` |
| Package a Hub block | `.ai/skills/custom-blocks` |
| Strengthen tests / local CI before a PR | `.cursor/skills/pre-merge-quality` |
| Open a fork PR once READY | `.cursor/skills/ci-guardrails` |
| Review the diff before a PR | `.ai/skills/self-review` |
| Env / first clone | `.cursor/skills/dev-setup` |
