---
name: request-intake
description: >
  Gather requirements and scope a Diffusers request before any code is
  written. Turns a vague ask into an intake brief (problem, acceptance
  criteria, change type, next skill). Use when a PM, product manager,
  stakeholder, researcher, or model author requests a new feature, new
  model, new pipeline, new scheduler, or feature request; when they say
  can we add, we should support, we'd like, is this in scope, gather
  requirements, scope this, write an issue, intake, acceptance criteria,
  problem statement; or when they mention a paper, arXiv, checkpoint,
  weights, or research repo without a classified engineering task.
---

# Request intake

PM / researcher front door. **Do not write library code.** Stop at a scoped
brief. If the user already named a change type and a file list, skip this
skill and use `.cursor/skills/scaffold-contribution` (or
`.ai/skills/model-integration` for a new model/pipeline).

Intake template: [reference.md](reference.md).

## 1. Restate

One sentence: who wants what, and why. If you cannot, ask — don't guess.

## 2. Ask what's missing

Ask only the gaps. Typical set:

- Who is this for (library user, training example, Hub checkpoint, paper repro)?
- Success criteria (what must work in a first PR)?
- Out of scope (LoRA, slow tests, extra workflows, training)?
- Modality (image / video / audio / 3D) and task (T2I, I2V, inpaint, …)
- In-tree neighbor or reference repo / paper / checkpoint if they have one
- Existing issue or PR (this fork or huggingface/diffusers)

Researchers often have a paper + weights and no file list. PMs often have
a user outcome and no architecture. Meet them there.

## 3. Search before recommending

Look for an existing issue, PR, or in-tree implementation (this repo and
the fork). Say if Hugging Face already has a thread — upstream still wants
coordination; **PRs from this kit still go to the fork.**

If you cannot name a closest in-tree reference and they didn't give a
repo/paper, say so. Do not browse random research code unless they pointed
at it (`.cursor/rules/boundaries.mdc`).

## 4. Recommend a type — or don't build

Use the `scaffold-contribution` type table. New transformer / VAE / UNet
or a new pipeline / modular blockset → **new model or pipeline** (not a
first-PR scaffold).

Valid outcomes: implement · docs-only · test-only · wait for a maintainer
· don't build yet.

## 5. Intake brief

Fill every section in [reference.md](reference.md). Optionally add a
GitHub issue body the user can paste. **No `src/` or `tests/` edits.**

## 6. Hand off

| Verdict | Next |
|---|---|
| Ready to implement (not a new model) | `.cursor/skills/scaffold-contribution` |
| New model / pipeline / paper port | `.ai/skills/model-integration` |
| Env not verified | `.cursor/skills/dev-setup` |
| Don't build / needs a maintainer | Stop. Leave the brief. |

Do not jump to `pre-merge-quality` or `ci-guardrails` from here.
