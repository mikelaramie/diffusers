# Diffusers Cursor agent kit — conversation recap

Saved from the Cursor chat that designed and landed this kit (14–15 Aug 2026).
Origin: `mikelaramie/diffusers`. **PRs go to this fork’s `main`, never `huggingface/diffusers`.**

## What this repo is

Hugging Face **Diffusers**: pretrained diffusion models (images, audio, video). Core pieces are **pipelines**, **schedulers**, and **models**. Conventions for agents live in `.ai/` (maintainer-owned on upstream). This kit lives in `.cursor/skills/` and `.cursor/rules/` so Cursor users get a first-day path without copying `.ai/`.

## Standing decisions

- One **project** skill/rule set, checked into the fork.
- Skills **link** to `.ai/`; they do not duplicate it.
- `make style` and clear new-code fixes are **applied** in `pre-merge-quality`.
- `ci-guardrails` **opens the fork PR once READY** (does not ask again). **NEEDS CHANGES** stops.
- Vague PM/researcher asks go through **`request-intake`** before any `src/` edits.
- `.cursor/` stays gitignored except `skills/` and `rules/`.

## Path a change should take

```
request-intake  →  (dev-setup if needed)  →  scaffold-contribution
        │                                         │
        └─ new model/pipeline → model-integration ┘
                                              ↓
                                    pre-merge-quality
                                              ↓ READY
                                        ci-guardrails  →  fork PR
```

`self-review` (`.ai/skills/self-review`) runs at the end of `pre-merge-quality`.

## Skills (`.cursor/skills/`)

| Skill | Role |
|---|---|
| `dev-setup` | Clone → `pip install -e ".[dev]"` → verify import + one CPU scheduler test. Never `make test`. |
| `request-intake` | PM/researcher front door. Requirements → intake brief. **No library code.** |
| `scaffold-contribution` | Classify change, copy one in-tree reference, smallest skeleton + change brief. |
| `pre-merge-quality` | Scan deprecated APIs / weak tests; scoped pytest; `make style` then `make quality`; then `self-review`; QA verdict. |
| `ci-guardrails` | Map diff → GitHub workflows; fill PR template; `gh pr create --repo mikelaramie/diffusers`. |

Existing `.ai/skills/` (not rewritten): `model-integration`, `self-review`, `diffusers-cli`, `custom-blocks`.

## Rules (`.cursor/rules/`)

| Rule | Scope |
|---|---|
| `boundaries.mdc` | **Always on.** Allowed context, no `.ai/` edits, no hand-edited `# Copied from`, unused params, **fork PRs only**. |
| `tests.mdc` | `tests/**/*.py` — real tiny dummies; no `@slow` / LoRA tests on an initial model PR. |
| `models.mdc` | `src/diffusers/models/**/*.py` → `.ai/models.md`; `dispatch_attention_fn`. |
| `pipelines.mdc` | `src/diffusers/pipelines/**/*.py` → `.ai/pipelines.md`; modular default; `@torch.no_grad` on `__call__`. |
| `modular.mdc` | `src/diffusers/modular_pipelines/**/*.py` → `.ai/modular.md`; `init_pipeline()`. |
| `inits.mdc` | `src/diffusers/**/__init__.py` — `_import_structure`. |
| `docs.mdc` | `docs/source/**/*.md` — `_toctree.yml`, Google docstrings. |

## PRs on the fork

| PR | What |
|---|---|
| [#1](https://github.com/mikelaramie/diffusers/pull/1) | `dev-setup` + un-ignore `.cursor/skills/` |
| [#2](https://github.com/mikelaramie/diffusers/pull/2) | `boundaries` + `tests` + `scaffold-contribution` |
| [#3](https://github.com/mikelaramie/diffusers/pull/3) | `pre-merge-quality` |
| [#4](https://github.com/mikelaramie/diffusers/pull/4) | `ci-guardrails` |
| [#5](https://github.com/mikelaramie/diffusers/pull/5) | `request-intake` |
| [#6](https://github.com/mikelaramie/diffusers/pull/6) | File-scoped convention rules (models/pipelines/modular/inits/docs) |

## Customer requirements (how we mapped them)

1. **Scaffold a first contribution** — `scaffold-contribution` (+ `dev-setup`, `request-intake`).
2. **Catch mistakes / strengthen tests** — `pre-merge-quality` + `tests.mdc` + `self-review`.
3. **CI / approved boundaries** — `ci-guardrails` + `boundaries.mdc`.
4. **Team can own it** — skills point at `.ai/`; this README is the map. Extend by adding a row to a skill table, not a new essay.
5. **Multi-role** — intake brief + change brief + QA + CI blocks (PM, engineer, QA, DevOps). Not a skill per audience.

## How to test a skill

Use a **new Agent chat** (not the one that wrote the skill). Example prompts:

- “I’m a new developer, get me contributing.” → `dev-setup`
- “Can we add this paper’s checkpoint?” → `request-intake` (no `src/` edits)
- “Add LoRA using Flux as the reference.” → `scaffold-contribution`
- “Ready for review.” → `pre-merge-quality` then, if READY, `ci-guardrails`

## Not built (on purpose)

- A skill per model or per role (PM-skill, QA-skill).
- Copying `.ai/models.md` into always-on rules.
- Release / PyPI / `make pre-release`.
- Extra scripts (`check_deprecated.py`) until the quality skill misses the same hit twice.
- `schedulers.mdc` — no `.ai/schedulers.md` yet.

## Chat thread (compressed)

1. Explained Diffusers; designed onboarding as **one** project skill (`dev-setup`).
2. Mapped five customer requirements; kept skills small; rules for always-on constraints.
3. Built and merged the kit in the order above.
4. Added PM/researcher **intake** so scaffolding is not the first step for a vague ask.
5. Added glob rules so conventions load when the matching source/docs files are open.
