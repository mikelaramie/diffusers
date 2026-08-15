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
- New public class not in the matching `__init__.py` lazy-import map
- New pipeline page not in `docs/source/en/_toctree.yml`

## Local commands (CI equivalents)

`pr_tests.yml` `check_code_quality` → `make quality` (after `make style`).

Do not run `make test`.
