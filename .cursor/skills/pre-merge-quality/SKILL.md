---
name: pre-merge-quality
description: >
  Run local CI-equivalent checks, scan a Diffusers diff for deprecated APIs
  and weak tests, apply make style plus clear new-code fixes, then hand off
  to self-review. Use when the user is ready for review, asks to strengthen
  tests, mentions deprecated APIs, pre-merge, or whether the change will
  pass CI.
---

# Pre-merge quality

Prove a contribution locally before review. **Act** on mechanical style and
clear new-code hits; **report** judgment calls. Then run
`.ai/skills/self-review` — do not duplicate that rubric here.

Canonical test rules: `.ai/testing.md` and `.cursor/rules/tests.mdc`.
Scan list: [reference.md](reference.md).

## 1. Scope the diff

```bash
git diff origin/main...HEAD
git diff
```

List touched paths under `src/`, `tests/`, and `docs/`. If the branch trails
`main` and the diff is polluted, scope to this branch's commits only.

## 2. Scan

Walk the diff against [reference.md](reference.md). Record each hit as
`path:line` · pattern · fix or leave.

## 3. Run local CI equivalents

Never `make test`.

- Touched tests: `python -m pytest tests/<path>/test_<thing>.py`
- `src/` or `tests/` changed: `make style`, then `make quality`
- New public classes: note that CI's `check_repository_consistency` also runs
  `utils/check_copies.py`, `utils/check_dummies.py`, `utils/check_inits.py`
  (via repo checks), and `utils/check_forward_call_docstrings.py`

If `make` is missing, use the commands in the top-level `Makefile` (`style`
and `quality` targets).

## 4. Fix vs report

**Apply now**

- `make style` (ruff fix/format, docstring style, dep table)
- Clear hits in *new* code only, for example:
  - `torch_dtype=` → `dtype=`
  - `unittest.TestCase` / `@unittest.skip` in a **new** pipeline test file → pytest
  - `@slow` / `LoraTesterMixin` on an *initial model* PR → remove
  - `SimpleNamespace` dummy in new tests → real class at tiny config

**Report only** (leave for the user or `self-review`)

- Changes in existing files that are unrelated drive-bys
- Dead code, philosophy, docs impact
- Whether a dedicated LoRA PR *should* add `tests/lora/…` (allowed; don't invent it)

Do not rewrite tests to "be safer." Strengthen them only when they violate
`.ai/testing.md`.

## 5. Self-review

After fixes, run `.ai/skills/self-review` on the **current** diff. Keep that
report separate from the QA block below.

## 6. QA block

Always end with:

```markdown
## QA
- **Commands run + results:**
- **Deprecated / anti-pattern findings:** fixed vs left (`path:line`)
- **Remaining risk:**
- **Verdict:** READY | NEEDS CHANGES
```

This fills the QA section of a `scaffold-contribution` change brief when one
exists. Do not open a PR from this skill — if the verdict is READY, the next
step is `.cursor/skills/ci-guardrails`.

## Hand off

| Next | Use |
|---|---|
| Open a fork PR (READY only) | `.cursor/skills/ci-guardrails` |
| Convention / dead-code review | `.ai/skills/self-review` (already run in step 5) |
| New model/pipeline | `.ai/skills/model-integration` |
| Scaffold a first change | `.cursor/skills/scaffold-contribution` |
