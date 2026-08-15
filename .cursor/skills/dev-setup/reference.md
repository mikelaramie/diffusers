# Diffusers repo map

Read this only when the user asks where something lives, or when picking
which tests/files to touch.

## Layout

| Path | What it is |
|---|---|
| `src/diffusers/pipelines/` | Inference pipelines (`DiffusionPipeline` subclasses) |
| `src/diffusers/modular_pipelines/` | Modular pipelines — preferred for new work |
| `src/diffusers/models/` | UNets, transformers, VAEs, and other building blocks |
| `src/diffusers/schedulers/` | Noise / sampling schedulers |
| `src/diffusers/loaders/` | Mixins for LoRA, single-file, IP-Adapter, etc. |
| `tests/` | Mirrors `src/diffusers/` (pipelines, models, schedulers, …) |
| `examples/` | Training scripts (DreamBooth, LoRA, ControlNet, …) |
| `docs/source/en/` | User-facing docs |
| `scripts/` | One-off conversion and maintenance scripts |
| `.ai/` | Agent conventions and task skills (maintainer-owned — do not edit in a contributor PR) |

New public classes are registered via lazy imports in the relevant `__init__.py`
files. Adding a class without wiring it there means `from diffusers import …`
will fail.

## Install extras

Defined in `setup.py`:

| Extra | Use |
|---|---|
| `[dev]` | Contributor default (quality + test + training + docs + torch) |
| `[test]` | Pytest and test-only deps |
| `[quality]` | Ruff, isort, doc-builder |
| `[torch]` | PyTorch + accelerate |

The Makefile sets `PYTHONPATH=src` so local commands hit this checkout.

## Tests

- Fast / default: `python -m pytest tests/<path>/test_<thing>.py`
- Slow tests (downloads real weights): `RUN_SLOW=yes python -m pytest …`
- Do not run `make test` during onboarding — it is the entire suite.

Convention for new model/pipeline tests: `.ai/testing.md`.

## Style and copies

- `make style` — ruff fix/format, docstring style, dep table, extra checks
- `make quality` — the same checks CI runs (no writes)
- `make fix-copies` — propagate `# Copied from` blocks from their source

If `make` is unavailable, the underlying commands are in the top-level
`Makefile` (`style`, `quality`, `fix-copies` targets).

## Agent guides (already in the repo)

- `.ai/AGENTS.md` — coding style, copied-code rule
- `.ai/models.md` / `.ai/pipelines.md` / `.ai/modular.md` — implementation conventions
- `.ai/testing.md` — required test layers and dummy-component rules
- `.ai/review-rules.md` — what reviewers (and `self-review`) check

## Fork sync

When updating a fork's `main` from upstream, merge directly into the fork.
Don't open a sync PR that @-mentions every upstream author. Details:
`docs/source/en/conceptual/contribution.md` ("Syncing forked main").
