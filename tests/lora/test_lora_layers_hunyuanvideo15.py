# Copyright 2026 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import unittest

import torch
from transformers import (
    AutoConfig,
    ByT5Tokenizer,
    Qwen2_5_VLTextConfig,
    Qwen2_5_VLTextModel,
    Qwen2Tokenizer,
    T5EncoderModel,
)

from diffusers import (
    AutoencoderKLHunyuanVideo15,
    FlowMatchEulerDiscreteScheduler,
    HunyuanVideo15ImageToVideoPipeline,
    HunyuanVideo15Pipeline,
    HunyuanVideo15Transformer3DModel,
)
from diffusers.guiders import ClassifierFreeGuidance

from ..testing_utils import floats_tensor, is_peft_available, require_peft_backend, skip_mps


if is_peft_available():
    from peft import LoraConfig


sys.path.append(".")

from .utils import PeftLoraLoaderMixinTests  # noqa: E402


@require_peft_backend
@skip_mps
class HunyuanVideo15LoRATests(unittest.TestCase, PeftLoraLoaderMixinTests):
    pipeline_class = HunyuanVideo15Pipeline
    scheduler_cls = FlowMatchEulerDiscreteScheduler
    scheduler_kwargs = {"shift": 7.0}

    transformer_kwargs = {
        "in_channels": 9,
        "out_channels": 4,
        "num_attention_heads": 2,
        "attention_head_dim": 8,
        "num_layers": 1,
        "num_refiner_layers": 1,
        "mlp_ratio": 2.0,
        "patch_size": 1,
        "patch_size_t": 1,
        "text_embed_dim": 16,
        "text_embed_2_dim": 32,
        "image_embed_dim": 12,
        "rope_axes_dim": (2, 2, 4),
        "target_size": 16,
        "task_type": "t2v",
    }
    transformer_cls = HunyuanVideo15Transformer3DModel
    vae_kwargs = {
        "in_channels": 3,
        "out_channels": 3,
        "latent_channels": 4,
        "block_out_channels": (16, 16),
        "layers_per_block": 1,
        "spatial_compression_ratio": 4,
        "temporal_compression_ratio": 2,
        "downsample_match_channel": False,
        "upsample_match_channel": False,
    }
    vae_cls = AutoencoderKLHunyuanVideo15
    has_two_text_encoders = True
    tokenizer_cls, tokenizer_id = Qwen2Tokenizer, "hf-internal-testing/tiny-random-Qwen2VLForConditionalGeneration"
    tokenizer_2_cls, tokenizer_2_id = ByT5Tokenizer, None
    text_encoder_cls, text_encoder_id = Qwen2_5_VLTextModel, None
    text_encoder_2_cls, text_encoder_2_id = T5EncoderModel, None

    supports_text_encoder_loras = False

    @property
    def output_shape(self):
        return (1, 9, 16, 16, 3)

    def get_dummy_inputs(self, with_generator=True):
        batch_size = 1
        sequence_length = 16
        num_channels = 4
        num_frames = 9
        num_latent_frames = (num_frames - 1) // 2 + 1
        sizes = (4, 4)

        generator = torch.manual_seed(0)
        noise = floats_tensor((batch_size, num_latent_frames, num_channels) + sizes)
        input_ids = torch.randint(1, sequence_length, size=(batch_size, sequence_length), generator=generator)

        pipeline_inputs = {
            "prompt": "monkey",
            "num_frames": num_frames,
            "num_inference_steps": 2,
            "height": 16,
            "width": 16,
            "output_type": "np",
        }
        if with_generator:
            pipeline_inputs.update({"generator": generator})

        return noise, input_ids, pipeline_inputs

    def get_dummy_components(self, scheduler_cls=None, use_dora=False, lora_alpha=None):
        torch.manual_seed(0)
        transformer = self.transformer_cls(**self.transformer_kwargs)

        torch.manual_seed(0)
        vae = self.vae_cls(**self.vae_kwargs)

        scheduler_cls = scheduler_cls if scheduler_cls is not None else self.scheduler_cls
        scheduler = scheduler_cls(**self.scheduler_kwargs)

        torch.manual_seed(0)
        qwen_config = Qwen2_5_VLTextConfig(
            hidden_size=16,
            intermediate_size=16,
            num_hidden_layers=2,
            num_attention_heads=2,
            num_key_value_heads=2,
            rope_scaling={
                "mrope_section": [1, 1, 2],
                "rope_type": "default",
                "type": "default",
            },
            rope_theta=1000000.0,
        )
        text_encoder = Qwen2_5_VLTextModel(qwen_config)
        tokenizer = Qwen2Tokenizer.from_pretrained(self.tokenizer_id)

        torch.manual_seed(0)
        t5_config = AutoConfig.from_pretrained("hf-internal-testing/tiny-random-t5")
        text_encoder_2 = T5EncoderModel(t5_config)
        tokenizer_2 = ByT5Tokenizer()

        rank = 4
        lora_alpha = rank if lora_alpha is None else lora_alpha

        text_lora_config = LoraConfig(
            r=rank,
            lora_alpha=lora_alpha,
            target_modules=self.text_encoder_target_modules,
            init_lora_weights=False,
            use_dora=use_dora,
        )
        denoiser_lora_config = LoraConfig(
            r=rank,
            lora_alpha=lora_alpha,
            target_modules=self.denoiser_target_modules,
            init_lora_weights=False,
            use_dora=use_dora,
        )

        pipeline_components = {
            "transformer": transformer,
            "vae": vae,
            "scheduler": scheduler,
            "text_encoder": text_encoder,
            "tokenizer": tokenizer,
            "text_encoder_2": text_encoder_2,
            "tokenizer_2": tokenizer_2,
            "guider": ClassifierFreeGuidance(guidance_scale=1.0),
        }
        return pipeline_components, text_lora_config, denoiser_lora_config

    def test_simple_inference_with_text_lora_denoiser_fused_multi(self):
        super().test_simple_inference_with_text_lora_denoiser_fused_multi(expected_atol=9e-3)

    def test_simple_inference_with_text_denoiser_lora_unfused(self):
        super().test_simple_inference_with_text_denoiser_lora_unfused(expected_atol=9e-3)

    def test_lora_state_dict_rejects_original_hunyuan_video_v1_keys(self):
        state_dict = {"double_blocks.0.img_attn_qkv.weight": torch.zeros(1, 1)}
        with self.assertRaisesRegex(ValueError, "img_attn_qkv"):
            self.pipeline_class.lora_state_dict(state_dict)

    def test_image_to_video_pipeline_exposes_load_lora_weights(self):
        self.assertTrue(hasattr(HunyuanVideo15ImageToVideoPipeline, "load_lora_weights"))
        self.assertIs(
            HunyuanVideo15ImageToVideoPipeline.load_lora_weights,
            HunyuanVideo15Pipeline.load_lora_weights,
        )

    @unittest.skip("Not supported in HunyuanVideo 1.5.")
    def test_simple_inference_with_text_denoiser_block_scale(self):
        pass

    @unittest.skip("Not supported in HunyuanVideo 1.5.")
    def test_simple_inference_with_text_denoiser_block_scale_for_all_dict_options(self):
        pass

    @unittest.skip("Not supported in HunyuanVideo 1.5.")
    def test_modify_padding_mode(self):
        pass
