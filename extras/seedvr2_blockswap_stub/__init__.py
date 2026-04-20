"""Compat stub for SeedVR2BlockSwap class (removed in SeedVR2 v2.x breaking change).

Original commit: numz/ComfyUI-SeedVR2_VideoUpscaler @ 5567f23 (2025-10-08) replaced
SeedVR2BlockSwap + SeedVR2ExtraArgs with SeedVR2LoadDiTModel / SeedVR2LoadVAEModel.
Older workflows (OFMTech 2.0 BarbecueMotion) still contain SeedVR2BlockSwap nodes
with orphaned outputs (0 links in the JSON), so they load with a red node in new
SeedVR2 versions.

This stub registers the class so the JSON loads clean. The output is a valid
block_swap_config dict (same shape as original), so even if someone DID wire it
to something, the shape is compatible.
"""


class SeedVR2BlockSwap:
    """Compatibility stub for SeedVR2BlockSwap (deprecated in SeedVR2 upstream)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "blocks_to_swap": ("INT", {"default": 16, "min": 0, "max": 36, "step": 1}),
                "offload_io_components": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("block_swap_config",)
    RETURN_NAMES = ("block_swap_config",)
    FUNCTION = "create_config"
    CATEGORY = "SEEDVR2"
    DESCRIPTION = (
        "Compat stub for legacy SeedVR2BlockSwap node (now configured on SeedVR2LoadDiTModel)."
    )

    def create_config(self, blocks_to_swap, offload_io_components):
        if blocks_to_swap == 0:
            return (None,)
        return ({
            "blocks_to_swap": blocks_to_swap,
            "offload_io_components": offload_io_components,
        },)


NODE_CLASS_MAPPINGS = {"SeedVR2BlockSwap": SeedVR2BlockSwap}
NODE_DISPLAY_NAME_MAPPINGS = {"SeedVR2BlockSwap": "SeedVR2 BlockSwap (compat stub)"}
