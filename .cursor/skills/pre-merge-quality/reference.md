# Pre-merge scan list

Check the **diff**, not the whole tree. Existing deprecated call sites that
this PR did not touch are out of scope.

## Deprecated APIs (new code)

| Avoid | Use instead |
|---|---|
| `torch_dtype=` | `dtype=` (`src/diffusers/utils/deprecation_utils.py`) |
| `CLIPFeatureExtractor` | `CLIPImageProcessor` |
| `_encode_prompt(` | `encode_prompt(` |
| `decode_latents` | `VaeImageProcessor.postprocess` / current decode helper |
| `LoraLoaderMixin` | the pipeline-specific `*LoraLoaderMixin` |
| New `deprecate(...)` for an API that never shipped | delete the shim (`.ai/AGENTS.md`) |

## Test anti-patterns

| Avoid | Use instead |
|---|---|
| `SimpleNamespace` / bare `nn.Module` dummies | Real class, tiny config (`tests/pipelines/wan/test_wan.py`) |
| Monkeypatch a component method to capture args | Call the real method; assert on state |
| `unittest.TestCase`, `setUp`/`tearDown`, `@unittest.skip` in **new** pipeline tests | pytest + `PipelineTesterMixin` / `MemoryTesterMixin` |
| `get_dummy_inputs(device, seed)` | `get_dummy_inputs()` + `self.get_generator(0)` |
| numpy round-trip image compare | `output_type="pt"` + `assert_tensors_close` |
| `@slow` / `RUN_SLOW` on an initial model/pipeline PR | omit; add later with maintainers |
| `LoraTesterMixin` / `tests/lora/test_lora_layers_*.py` on an *initial model* PR | omit; allowed on a dedicated LoRA PR |

## Other

- `# Copied from` block edited by hand → change the source, `make fix-copies`
- New public library class not in the matching `__init__.py` lazy-import map
- New docs page not in `docs/source/<lang>/_toctree.yml`
- Community pipeline: more than one `DiffusionPipeline` subclass in the file, or missing `register_modules`; README table row missing
- Official training example: missing `requirements.txt`, README command, or `test_*.py`
- Research example: missing maintainer `@handle` in the README
- New model / pipeline / scheduler that fights `docs/source/en/conceptual/philosophy.md` (silent fallbacks, fused model+scheduler, new arch in an existing file)

## Local commands (CI equivalents)

`pr_tests.yml` `check_code_quality` → `make quality` (after `make style`).
`examples/**/*.py` also trips `pr_tests.yml`.

Do not run `make test`.
