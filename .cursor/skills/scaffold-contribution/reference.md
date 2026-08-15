# Scaffold reference

Read this when classifying a change or listing files to create.

## File layouts by type

### LoRA / loader (existing pipeline)

Add a mixin to the existing loader file; don't start a new module unless the family is new.

```
src/diffusers/loaders/lora_pipeline.py   # add <Model>LoraLoaderMixin next to the closest sibling
src/diffusers/pipelines/<model>/pipeline_*.py   # inherit the mixin
src/diffusers/__init__.py                # lazy-import the mixin if it is public
tests/lora/test_lora_layers_<model>.py   # only on a dedicated LoRA PR — copy tests/lora/test_lora_layers_flux.py
```

Initial **model** PRs must not add LoRA tests (`.ai/testing.md`). A follow-up LoRA PR may.

### Scheduler

```
src/diffusers/schedulers/scheduling_<name>.py
src/diffusers/schedulers/__init__.py
src/diffusers/__init__.py
tests/schedulers/test_scheduler_<name>.py
```

### Bugfix / test-only

Touch the failing production file and the matching test under `tests/` that already mirrors it (`tests/pipelines/…`, `tests/models/…`, `tests/schedulers/…`). Don't add a new test module unless none exists.

### Docs

```
docs/source/en/api/… or docs/source/en/using-diffusers/…
docs/source/en/_toctree.yml          # required for a new page
```

Docstrings: Google style. See `docs/source/en/conceptual/contribution.md`.

### New model / pipeline

Not this skill. File list and checklist: `.ai/skills/model-integration`.
Conventions: `.ai/models.md`, `.ai/pipelines.md`, `.ai/modular.md`.
Tests: `.ai/testing.md`. Prefer modular for new pipelines.

## Reference picks (start here)

| You are adding… | Read first |
|---|---|
| Flux-like LoRA | `FluxLoraLoaderMixin` in `src/diffusers/loaders/lora_pipeline.py`, `tests/lora/test_lora_layers_flux.py` |
| Video LoRA (Wan / Hunyuan / LTX) | The closest `*LoraLoaderMixin` in the same file (e.g. `HunyuanVideoLoraLoaderMixin`) |
| Standard pipeline tests | `tests/pipelines/flux/test_pipeline_flux.py` |
| Modular pipeline tests | `tests/modular_pipelines/flux2/test_modular_pipeline_flux2_klein.py` |
| Scheduler tests | `tests/schedulers/test_scheduler_ddim.py` |
| Dummy size scale | `tests/pipelines/wan/test_wan.py` (`get_dummy_components`) |

## Lazy imports

New public classes must be listed in the matching `_import_structure` / `__init__.py`.
`from diffusers import Foo` fails if you add the class file but skip the map.

## Local checks (not the full suite)

```bash
python -m pytest tests/<path>/test_<thing>.py
make style
```

Do not run `make test`.
