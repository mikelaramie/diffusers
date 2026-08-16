# Diffusers Cursor agent kit

Origin: `mikelaramie/diffusers`. **PRs go to this fork’s `main`, never `huggingface/diffusers`.**
The user of this kit is the **maintainer of this fork** — confirming an intake
brief or scaffold plan is the ack. Do not wait on upstream.

Handbook: `docs/source/en/conceptual/contribution.md`.
Design constitution: `docs/source/en/conceptual/philosophy.md`
(required before adding a model, pipeline, or scheduler).

## Standing decisions

- One **project** skill/rule set, checked into the fork.
- Skills **link** to `.ai/` and the two conceptual docs; they do not paste them.
- `make style` and clear new-code fixes are **applied** in `pre-merge-quality`.
- `ci-guardrails` **opens the fork PR once READY**. **NEEDS CHANGES** stops.
- Vague asks go through **`request-intake`** before any `src/` / `examples/` edits.
- `.cursor/` stays gitignored except `skills/` and `rules/`.
- Do not edit `.ai/` unless the user asked to change agent conventions.

## Path a change should take

```
request-intake  →  (dev-setup if needed)  →  scaffold-contribution
        │                                         │
        ├─ new model/pipeline → model-integration ┤
        ├─ Hub custom block → custom-blocks       ┤
        └─ forum / Discord / don't build → stop   ┘
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
| `request-intake` | Front door. Channel (forum vs issue) + type + intake brief. **No library code.** |
| `scaffold-contribution` | Classify, copy one in-tree reference, smallest skeleton + change brief. |
| `pre-merge-quality` | Scan deprecated APIs / weak tests / philosophy conflicts; scoped pytest; `make style` then `make quality`; then `self-review`; QA verdict. |
| `ci-guardrails` | Map diff → GitHub workflows; fill PR template; `gh pr create --repo mikelaramie/diffusers`. |

Existing `.ai/skills/` (not rewritten): `model-integration`, `self-review`, `diffusers-cli`, `custom-blocks`.

## Change types this kit covers

From the contribution guide, plus Hub/CLI:

| Type | Where | Skill |
|---|---|---|
| Usage question / writeup | Forum (preferred) or Discord | `request-intake` → stop |
| Bug / API feedback / feature issue | This-fork issue | `request-intake` |
| Bugfix, docs, tests | `src/` / `tests/` / `docs/` | `scaffold-contribution` |
| Scheduler | `src/diffusers/schedulers/` | scaffold (read **philosophy** first) |
| Community pipeline | `examples/community/` | `scaffold-contribution` |
| Official training example | `examples/<name>/` | `scaffold-contribution` |
| Research training example | `examples/research_projects/` | `scaffold-contribution` |
| LoRA / loader mixin | `src/diffusers/loaders/` | `scaffold-contribution` |
| New model / pipeline | `src/diffusers/{models,pipelines,modular_pipelines}/` | `model-integration` (read **philosophy** first) |
| Hub custom modular block | Hub repo | `custom-blocks` |
| Run / inspect a pipeline | CLI | `diffusers-cli` |

## Rules (`.cursor/rules/`)

| Rule | Scope |
|---|---|
| `boundaries.mdc` | **Always on.** Allowed context, philosophy, no casual `.ai/` edits, **fork PRs only**, user is maintainer. |
| `tests.mdc` | `tests/**/*.py` — real tiny dummies; no `@slow` / LoRA on an *initial model* PR. |
| `models.mdc` | `src/diffusers/models/**/*.py` → `.ai/models.md` + philosophy. |
| `pipelines.mdc` | `src/diffusers/pipelines/**/*.py` → `.ai/pipelines.md` + philosophy; community vs core. |
| `modular.mdc` | `src/diffusers/modular_pipelines/**/*.py` → `.ai/modular.md` + philosophy. |
| `schedulers.mdc` | `src/diffusers/schedulers/**/*.py` → philosophy Schedulers section. |
| `examples.mdc` | `examples/**` — community vs official vs research. |
| `inits.mdc` | `src/diffusers/**/__init__.py` — `_import_structure`. |
| `docs.mdc` | `docs/source/**/*.md` — `_toctree.yml`, Google docstrings, translations. |

## How to test a skill

Use a **new Agent chat** (not the one that wrote the skill). Example prompts:

- “I’m a new developer, get me contributing.” → `dev-setup`
- “Can we add this paper’s checkpoint?” → `request-intake` (no `src/` edits)
- “Add a community pipeline like one_step_unet.” → `scaffold-contribution`
- “New DreamBooth-style training example.” → `scaffold-contribution`
- “Add LoRA using Flux as the reference.” → `scaffold-contribution`
- “Ready for review.” → `pre-merge-quality` then, if READY, `ci-guardrails`

## Not built (on purpose)

- A skill per model or per role (PM-skill, QA-skill).
- Copying `.ai/models.md` or the philosophy essay into always-on rules.
- Release / PyPI / `make pre-release`.
- Extra scripts (`check_deprecated.py`) until the quality skill misses the same hit twice.
