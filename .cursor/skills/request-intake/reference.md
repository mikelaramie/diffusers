# Intake brief

Copy and fill. PM, researcher, and engineer share this artifact.

```markdown
## Intake brief

- **Ask (one sentence):**
- **Who / source:** PM · researcher · model author · user — plus paper / repo / checkpoint if any
- **Channel:** this-fork issue · forum · Discord · none needed
- **Success criteria (first PR):**
- **Out of scope:**
- **Proposed change type:** (see table below)
- **Philosophy check (model / pipeline / scheduler only):** read `docs/source/en/conceptual/philosophy.md` — pass / conflict (say which)
- **Closest in-tree reference:** path or "none found"
- **Existing issue / PR (this fork):** link or none
- **Next skill:** scaffold-contribution · model-integration · custom-blocks · diffusers-cli · dev-setup · stop
```

Optional GitHub issue body (this fork). One issue per problem.

```markdown
## Summary
<precise title-worthy ask>

## Repro (bugs)
```python
# copy-paste into a Python shell — no missing imports
```

```
# paste `diffusers-cli env`
```

## Acceptance criteria
- [ ]

## Out of scope

## Reference
- In-tree:
- Paper / repo / checkpoint:

## Proposed approach
Change type + next skill
```

## Change types

Same table as `scaffold-contribution`. Use it to pick **next**, not to write files.

| Type | Next |
|---|---|
| New model or pipeline | `.ai/skills/model-integration` (read philosophy first) |
| Scheduler, community pipeline, official example, research example, LoRA/loader, bugfix, test-only, docs | `.cursor/skills/scaffold-contribution` (scheduler: read philosophy first) |
| Hub custom modular block | `.ai/skills/custom-blocks` |
| Run / inspect a pipeline from the terminal | `.ai/skills/diffusers-cli` |
| Usage question / writeup | forum (preferred) or Discord — stop |
| Don't build | stop |

Human handbook: `docs/source/en/conceptual/contribution.md`.
