---
name: dev-setup
description: >
  Set up a local Diffusers contributor environment and walk a new developer
  through a first change. Use when cloning the repo, installing from source,
  onboarding, getting started contributing, running the first tests, or
  asking how to open a first PR.
---

# Diffusers contributor setup

Get a new developer from clone to a verified editable install, then a small
correct first change. Do the steps; don't lecture about diffusion theory.

Read [reference.md](reference.md) only for the repo map or command details.
Handbook: `docs/source/en/conceptual/contribution.md`.
Philosophy (before adding a model, pipeline, or scheduler):
`docs/source/en/conceptual/philosophy.md`.

PRs from this kit go to **this fork's** `main` (`mikelaramie/diffusers`).
The user is the maintainer of this fork.

## 1. Prerequisites

- Python **>= 3.10** (`python_requires` in `setup.py`)
- A virtualenv (create one if the user isn't already in one)
- Git; they should work on a **feature branch**, never `main`
- GPU is optional. Unit tests and schedulers run on CPU.
- A Hugging Face token is **not** required for setup or most unit tests.
  Only needed for gated Hub models.

If `python --version` is too old, stop and say so. Don't improvise.

## 2. Install

From the repo root, in the venv:

```bash
pip install -e ".[dev]"
```

`[dev]` is quality + test + training + docs + torch. That is the contributor
install. Don't suggest `pip install diffusers` (that's PyPI, not this checkout).

## 3. Verify (required)

Run these, in order. Stop if one fails.

```bash
python -c "import diffusers; print(diffusers.__version__)"
```

Expect a `.dev0` version (this checkout), not a released PyPI version.

```bash
python -m pytest tests/schedulers/test_scheduler_ddim.py -q
```

This is CPU-only and needs no Hub download. **Do not** run `make test` —
the full suite is huge.

Optional, only if they want a real pipeline smoke test and have network:

```python
from diffusers import DiffusionPipeline
pipe = DiffusionPipeline.from_pretrained(
    "hf-internal-testing/tiny-stable-diffusion-pipe", safety_checker=None
)
```

## 4. Daily contributor commands

| Task | Command |
|---|---|
| Tests for what you touched | `python -m pytest tests/<path>/test_<thing>.py` |
| Official example tests | `python -m pytest examples/<name>/test_<name>.py` |
| Format + autofix | `make style` |
| Lint (CI-equivalent check) | `make quality` |
| Sync `# Copied from` blocks | `make fix-copies` |
| Bug-report environment | `diffusers-cli env` |

Rules the agent must follow:

- Never edit a `# Copied from ...` block by hand — change the source, then
  `make fix-copies`. Remove the header only to intentionally break the link.
- Don't add fallback paths, unused params, or "just in case" config.
- Conventions live in `.ai/AGENTS.md`. Read that before writing library code.
- Don't edit `.ai/` unless the user asked to change agent conventions.

## 5. First contribution

1. Confirm the env from steps 2–3 is green.
2. If the ask is vague, run `.cursor/skills/request-intake`. Valid first
   changes include a bugfix, docs, a scheduler, a community pipeline, a
   training example, tests, or a LoRA mixin — not only a new model.
3. New model/pipeline → stop and use `.ai/skills/model-integration` (read
   philosophy first). Experimental inference that is not a new architecture
   → `examples/community`, not `src/`.
4. `git checkout -b <descriptive-name>` off up-to-date `main`.
5. Make the smallest change that matches the type.
6. Run **only** the affected tests, then `make style`.
7. Before opening a PR, run `.cursor/skills/pre-merge-quality` (it runs
   `.ai/skills/self-review`). Share that report on the PR.
8. Open the PR on **this fork** with `.cursor/skills/ci-guardrails`.

## Which existing skill next

| They want to… | Use |
|---|---|
| Scope a vague / PM / researcher ask | `.cursor/skills/request-intake` |
| Scaffold a classified change | `.cursor/skills/scaffold-contribution` |
| Add/convert a model or pipeline | `.ai/skills/model-integration` |
| Package a modular block for the Hub | `.ai/skills/custom-blocks` |
| Run or inspect a pipeline from the CLI | `.ai/skills/diffusers-cli` |
| Local CI + strengthen tests | `.cursor/skills/pre-merge-quality` |
| Open a fork PR | `.cursor/skills/ci-guardrails` |
| Review a diff before a PR | `.ai/skills/self-review` |
