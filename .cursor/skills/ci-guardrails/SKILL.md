---
name: ci-guardrails
description: >
  Map a Diffusers diff to the CI workflows it will hit, fill the PR template
  from the change brief and QA verdict, and open a pull request on this fork
  once pre-merge-quality is READY. Use when opening a PR, asking what CI
  runs, or whether a change will pass CI.
---

# CI guardrails

Last mile: open a fork PR that matches what CI will run. Do not re-scan
deprecated APIs or rewrite tests — that is `.cursor/skills/pre-merge-quality`.

Workflow path map: [reference.md](reference.md).
PR target: `mikelaramie/diffusers` `main` (`.cursor/rules/boundaries.mdc`).

## 1. Gate

If there is no QA verdict of **READY** from `pre-merge-quality` in this
session, run that skill first.

- **READY** → continue and **open the PR** on this fork (do not ask again).
  The user is the maintainer; the intake/plan confirmation already was the ack.
  Do not wait for `huggingface/diffusers`.
- **NEEDS CHANGES** → stop. Do not open a PR.

## 2. Map CI

From `git diff origin/main...HEAD`, list workflows that match `on.paths` in
[reference.md](reference.md). Say which will actually run on **this fork**
vs only on upstream (GPU, style bot, `@claude`).

## 3. Do not

- `--repo huggingface/diffusers`
- Add or edit `.github/workflows` unless the user asked
- Add secrets, `RUN_SLOW`, or Hub weight downloads in fast tests
- Run `make test` or invent extra CI jobs

## 4. Open the PR

```bash
git push -u origin HEAD
gh pr create --repo mikelaramie/diffusers --base main --head <branch>
```

Fill `.github/PULL_REQUEST_TEMPLATE.md`:

- Summary from the change brief
- Issue / coordination link if one exists on **this fork** (not required if
  the user already confirmed the intake brief)
- Test commands + results from the QA block
- Final self-review notes (or say they will be a PR comment)
- AI-agent checklist ticked honestly

## 5. CI block

Always end with:

```markdown
## CI
- **Workflows this path should hit:**
- **Local equivalents already run:**
- **Fork vs upstream:** what will not run here (GPU, style bot, @claude)
- **PR:** <url>
```

## Hand off

| Next | Use |
|---|---|
| Local checks not done yet | `.cursor/skills/pre-merge-quality` |
| Convention report | `.ai/skills/self-review` |
| Scaffold a change | `.cursor/skills/scaffold-contribution` |
| Vague / PM / researcher ask | `.cursor/skills/request-intake` |
