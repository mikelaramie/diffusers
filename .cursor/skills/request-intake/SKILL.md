---
name: request-intake
description: >
  Gather requirements and scope a Diffusers request before any code is
  written. Turns a vague ask into an intake brief (problem, acceptance
  criteria, change type, next skill). Use when a PM, product manager,
  stakeholder, researcher, or model author requests a new feature, new
  model, new pipeline, new scheduler, community pipeline, training
  example, docs change, or bugfix; when they say can we add, we should
  support, we'd like, is this in scope, gather requirements, scope this,
  write an issue, intake, acceptance criteria, problem statement, good
  first issue, forum, Discord; or when they mention a paper, arXiv,
  checkpoint, weights, research repo, DreamBooth, or research_projects
  without a classified engineering task.
---

# Request intake

Front door for any Diffusers request. **Do not write library code.** Stop at a
scoped brief. If the user already named a change type and a file list, skip
this skill and use `.cursor/skills/scaffold-contribution` (or
`.ai/skills/model-integration` for a new model/pipeline).

Canonical types and issue template: [reference.md](reference.md).
Human handbook: `docs/source/en/conceptual/contribution.md`.
Design constitution (models / pipelines / schedulers):
`docs/source/en/conceptual/philosophy.md`.

You are talking to the **maintainer of this fork**. Confirming the intake
brief **is** the ack. Do not wait for `huggingface/diffusers`. PRs from this
kit still go to `mikelaramie/diffusers` `main`.

## 1. Restate

One sentence: who wants what, and why. If you cannot, ask — don't guess.

## 2. Ask what's missing

Ask only the gaps. Typical set:

- Who is this for (library user, training example, Hub checkpoint, paper repro)?
- Success criteria (what must work in a first PR)?
- Out of scope
- Modality (image / video / audio / 3D) and task (T2I, I2V, inpaint, …)
- In-tree neighbor or reference repo / paper / checkpoint if they have one
- Existing issue or PR on **this fork** (mention an upstream thread only as context)

Researchers often have a paper + weights and no file list. PMs often have
a user outcome and no architecture. Meet them there.

## 3. Search before recommending

Look for an existing issue, PR, or in-tree implementation **on this fork
first**. Upstream huggingface/diffusers threads are context, not a PR target
and not a blocker.

If you cannot name a closest in-tree reference and they didn't give a
repo/paper, say so. Do not browse random research code unless they pointed
at it (`.cursor/rules/boundaries.mdc`).

## 4. Route: channel, then type

**Not a code change**

| Ask | Where |
|---|---|
| Usage question, experiment writeup, personal project | Forum (preferred) or Discord — not GitHub, not a PR |
| Bug, API feedback, feature, new component | Issue on this fork, then a change type below |

A high-quality issue is precise, minimal, and reproducible. For a bug: a
copy-paste snippet, `diffusers-cli env`, and no extra libraries. Template:
[reference.md](reference.md).

**Code change — pick one type** from the table in [reference.md](reference.md).
Core vs community vs Hub:

- New SOTA architecture for the library → `src/` (new model / pipeline / scheduler). **Read philosophy first.**
- Experimental / one-off inference trick → `examples/community` (GitHub) or a Hub `custom_pipeline`
- Shareable modular block, no core change → `.ai/skills/custom-blocks`
- How-to training script → official `examples/` or `examples/research_projects`
- Run or inspect a pipeline from a terminal → `.ai/skills/diffusers-cli` (not a PR)

If the type is **new model, pipeline, or scheduler**, read
`docs/source/en/conceptual/philosophy.md` before recommending. If the design
fights it (silent fallbacks, fused model+scheduler, new arch stuffed into an
existing file, extra hard dependency), say so in the brief — do not plan
around it.

Valid outcomes: implement · docs-only · test-only · forum/Discord · don't
build yet.

## 5. Intake brief

Fill every section in [reference.md](reference.md). Optionally add a
GitHub issue body the user can paste. **No `src/`, `tests/`, or `examples/`
edits.**

## 6. Hand off

| Verdict | Next |
|---|---|
| Ready to implement (not a new model/pipeline) | `.cursor/skills/scaffold-contribution` |
| New model / pipeline / paper port | `.ai/skills/model-integration` |
| Hub custom block | `.ai/skills/custom-blocks` |
| CLI run / schema | `.ai/skills/diffusers-cli` |
| Env not verified | `.cursor/skills/dev-setup` |
| Forum / Discord / don't build | Stop. Leave the brief. |

Do not jump to `pre-merge-quality` or `ci-guardrails` from here.
