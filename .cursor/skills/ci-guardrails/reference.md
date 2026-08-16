# CI path map

Read the workflow YAML `on.paths` if unsure. This table is the usual case
for a PR into `main`.

| Paths touched | Workflow | Local equivalent |
|---|---|---|
| `src/diffusers/**/*.py`, `tests/**`, `utils/`, `scripts/`, `examples/**/*.py`, `setup.py`, `.github/**.yml` | `pr_tests.yml` — `make quality`, repo consistency, fast CPU tests | `make style` && `make quality`; scoped `pytest` |
| `src/diffusers/modular_pipelines/**`, `tests/modular_pipelines/**` | `pr_modular_tests.yml` as well | scoped modular pytest |
| `docs/**` or `src/diffusers/**/*.py` or `examples/**` | `build_pr_documentation.yml` | don't invent a local doc build unless docs changed and the user wants it |
| `examples/community/**` | `pr_tests.yml` (Python) + docs build if README/table changed | scoped pytest usually N/A; `make style` if `.py` changed |
| `src/diffusers/loaders/lora_*.py`, `peft.py`, `pipeline_utils.py`, `pipeline_loading_utils.py`, `modeling_utils.py`, `model_loading_utils.py`, `tests/pipelines/test_pipelines_common.py`, `tests/models/test_modeling_common.py`, `examples/**/*.py` | `pr_tests_gpu.yml` | often **absent on this fork** |
| Maintainer comment `@claude` | `claude_review.yml` | not automatic |
| Style-bot comment | `pr_style_bot.yml` | needs HF bot secrets; **won't work the same on this fork** |

Repo consistency inside `pr_tests.yml` also runs:

```bash
python utils/check_copies.py
python utils/check_dummies.py
python utils/check_support_list.py
python utils/check_forward_call_docstrings.py
make deps_table_check_updated
```

`pre-merge-quality` already covers `make style` / `make quality` and scoped
pytest. Do not run `make test`.

## Fork vs upstream

This repo's origin is `mikelaramie/diffusers`. Open PRs there. GPU runners,
the HF style bot, and `@claude` review are upstream-maintainer machinery —
note them in the CI block; don't try to recreate them.
