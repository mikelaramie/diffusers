# Scaffold reference

Read this when classifying a change or listing files to create.

Handbook: `docs/source/en/conceptual/contribution.md`.
Philosophy (required for new models, pipelines, schedulers):
`docs/source/en/conceptual/philosophy.md`.

## File layouts by type

### Scheduler

One algorithm per file. Inherit `SchedulerMixin` + `ConfigMixin`. Expose
`set_num_inference_steps`, `step`, and `timesteps`. Do not import from large
utils modules. Novel sampler → new file, not a fork of an existing class.

```
src/diffusers/schedulers/scheduling_<name>.py
src/diffusers/schedulers/__init__.py
src/diffusers/__init__.py
tests/schedulers/test_scheduler_<name>.py
```

Reference: `scheduling_ddim.py` + `tests/schedulers/test_scheduler_ddim.py`.

### Community pipeline

GitHub community pipelines live in `examples/community/`. One
`DiffusionPipeline` subclass per file, `register_modules` in `__init__`,
one `__call__`. Soft deps are OK if the user installs them. Not a core
architecture — those go to `model-integration`.

```
examples/community/<name>.py
examples/community/README.md          # add a table row (author + short description)
```

Tutorial file: `examples/community/one_step_unet.py`.
Hub-only `custom_pipeline` (no GitHub file): do not open a library PR;
upload the file to a Hub repo instead.

### Official training example

Single-file script, CLI (`python train_….py --args`), Accelerate,
`requirements.txt`, README with a command and expected results. Add a test
in the same folder.

```
examples/<name>/train_<name>.py
examples/<name>/requirements.txt
examples/<name>/README.md
examples/<name>/test_<name>.py
```

Reference: `examples/dreambooth/` (`train_dreambooth.py`, `test_dreambooth.py`).

### Research training example

Same layout under `examples/research_projects/<name>/`. No test required.
README must say who maintains it (`@handle`). Experimental / not-yet-popular
training belongs here, not in official `examples/`.

Reference: `examples/research_projects/intel_opts/README.md` (maintainer line).

### LoRA / loader (existing pipeline)

Add a mixin to the existing loader file; don't start a new module unless
the family is new.

```
src/diffusers/loaders/lora_pipeline.py   # add <Model>LoraLoaderMixin next to the closest sibling
src/diffusers/pipelines/<model>/pipeline_*.py   # inherit the mixin
src/diffusers/__init__.py                # lazy-import the mixin if it is public
tests/lora/test_lora_layers_<model>.py   # only on a dedicated LoRA PR — copy tests/lora/test_lora_layers_flux.py
```

Initial **model** PRs must not add LoRA tests (`.ai/testing.md`). A follow-up
LoRA PR may.

### Bugfix / test-only

Touch the failing production file and the matching test under `tests/` that
already mirrors it (`tests/pipelines/…`, `tests/models/…`,
`tests/schedulers/…`, `examples/<name>/test_*.py`). Don't add a new test
module unless none exists.

### Docs

```
docs/source/<lang>/api/… or docs/source/<lang>/using-diffusers/… or conceptual/…
docs/source/<lang>/_toctree.yml          # required for a new page
```

Docstrings: Google style. No images/videos in the repo — host on
`hf-internal-testing` or `huggingface/documentation-images`.
Translations: same path under `docs/source/<lang>/`.

### New model / pipeline

Not this skill. File list and checklist: `.ai/skills/model-integration`.
Read philosophy first. Conventions: `.ai/models.md`, `.ai/pipelines.md`,
`.ai/modular.md`. Tests: `.ai/testing.md`. Prefer modular for new pipelines.

## Reference picks (start here)

| You are adding… | Read first |
|---|---|
| Scheduler | `src/diffusers/schedulers/scheduling_ddim.py`, `tests/schedulers/test_scheduler_ddim.py` |
| Community pipeline | `examples/community/one_step_unet.py`, then the closest `examples/community/pipeline_*.py` |
| Official training example | `examples/dreambooth/train_dreambooth.py` + `test_dreambooth.py` + `README.md` |
| Research training example | `examples/research_projects/intel_opts/README.md` (maintainer blurb) |
| LoRA mixin | closest `*LoraLoaderMixin` in `src/diffusers/loaders/lora_pipeline.py`; Flux tests as the LoRA-PR template |
| Standard pipeline tests | `tests/pipelines/flux/test_pipeline_flux.py` |
| Modular pipeline tests | `tests/modular_pipelines/flux2/test_modular_pipeline_flux2_klein.py` |
| Dummy size scale | `tests/pipelines/wan/test_wan.py` (`get_dummy_components`) |

## Lazy imports

New **public library** classes must be listed in the matching
`_import_structure` / `__init__.py`. `from diffusers import Foo` fails if
you add the class file but skip the map. Skip this for `examples/community`
and training scripts.

## Local checks (not the full suite)

```bash
python -m pytest tests/<path>/test_<thing>.py   # library tests
python -m pytest examples/<name>/test_<name>.py # official examples only
make style
```

Do not run `make test`.
