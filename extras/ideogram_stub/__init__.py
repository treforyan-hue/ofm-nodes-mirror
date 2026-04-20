"""IdeogramEditImage stub — custom node.

Оригинал в private репо `instara-io/ComfyUI_INSTARAW` (INSTARAW API nodes).
В воркфлоу faceswap.json используется API Ideogram v3 Edit.

Нода в workflow помечена mode=4 (bypassed by default), поэтому passthrough безопасен.
Если user получит доступ к private INSTARAW пакету — stub перезапишется реальным.

Сигнатура восстановлена из workflow:
- INPUT: api_key (STRING), provider (STRING), image (IMAGE), mask (MASK),
         character_reference_image (IMAGE, optional)
- WIDGETS: prompt (STRING multiline), magic_prompt_option (ENUM), style_type (ENUM),
           seed (INT), seed_control (ENUM)
- OUTPUT: IMAGE
"""


class IdeogramEditImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "provider": ("STRING", {"default": "ideogram"}),
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "magic_prompt_option": (["TURBO", "DEFAULT", "OFF"], {"default": "DEFAULT"}),
                "style_type": (["AUTO", "GENERAL", "REALISTIC", "DESIGN", "ANIME",
                                "ON", "OFF"], {"default": "AUTO"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "seed_control": (["fixed", "randomize"], {"default": "randomize"}),
            },
            "optional": {
                "character_reference_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "edit"
    CATEGORY = "INSTARAW/stub"

    def edit(self, api_key, provider, image, mask, prompt, magic_prompt_option,
             style_type, seed, seed_control, character_reference_image=None):
        # Stub: passthrough оригинал без изменений.
        # Реальная реализация в private instara-io/ComfyUI_INSTARAW
        # использует Ideogram v3 Edit API.
        return (image,)


NODE_CLASS_MAPPINGS = {"IdeogramEditImage": IdeogramEditImage}
NODE_DISPLAY_NAME_MAPPINGS = {"IdeogramEditImage": "Ideogram Edit Image (stub)"}
