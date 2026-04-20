"""YANC.SaveImageWEBP stub — custom node.

Upstream ALatentPlace/ComfyUI_yanc НЕ содержит класса YANC.SaveImageWEBP.
PR #6708 в comfyanonymous/ComfyUI закрыт. Форки (10 шт) тоже не имеют.

Этот stub воспроизводит класс с нужной сигнатурой:
- inputs: images, filename_prefix, subfolder, embed_workflow, quality
- output: None (OUTPUT_NODE)
- behaviour: сохраняет WEBP через PIL с указанным quality

Используется в флоу: darkhub_z_image (darkhub_zimage.json).
"""
import json
import os

import numpy as np
from PIL import Image

import folder_paths
from comfy.cli_args import args


class YANCSaveImageWEBP:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "output"}),
                "subfolder": ("STRING", {"default": ""}),
                "embed_workflow": ("BOOLEAN", {"default": False}),
                "quality": ("INT", {"default": 90, "min": 1, "max": 100}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "YANC/image"

    def save(self, images, filename_prefix, subfolder, embed_workflow, quality,
             prompt=None, extra_pnginfo=None):
        out_dir = os.path.join(self.output_dir, subfolder) if subfolder else self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        results = []
        for i, img in enumerate(images):
            arr = (255.0 * img.cpu().numpy()).clip(0, 255).astype(np.uint8)
            pil = Image.fromarray(arr)
            fn = f"{filename_prefix}_{i:05d}.webp"
            path = os.path.join(out_dir, fn)
            kw = {"quality": int(quality), "method": 6}
            if embed_workflow and not args.disable_metadata and (prompt or extra_pnginfo):
                exif = Image.Exif()
                exif[0x9286] = json.dumps({"prompt": prompt, "workflow": extra_pnginfo})
                kw["exif"] = exif.tobytes()
            pil.save(path, format="WEBP", **kw)
            results.append({"filename": fn, "subfolder": subfolder, "type": self.type})
        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {"YANC.SaveImageWEBP": YANCSaveImageWEBP}
NODE_DISPLAY_NAME_MAPPINGS = {"YANC.SaveImageWEBP": "> Save Image as WEBP (YANC stub)"}
