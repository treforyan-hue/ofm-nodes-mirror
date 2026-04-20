"""RHHiddenNodes stub — custom node.

Оригинал: проприетарные ноды RunningHub (runninghub.ai), server-side only,
исходный код не публикуется (подтверждено в Comfy-Org/ComfyUI discussion #9796).

Семантика (traced из action_transfer.json):
- 7 inputs: pwd (STRING), image_1, width_2, height_3, image_4, width_5, height_6
- 11 outputs: p0, IMAGE_1, IMAGE_2, width_3, height_4, IMAGE_5, IMAGE_6,
              width_7, width_8, height_9, height_10

Реверс-инженеринг показывает что это pwd-gated multiplexer/router — сервер
валидирует pwd и раздаёт inputs в outputs (без transformations).
Stub игнорирует pwd и прокидывает значения наружу.

Используется в флоу: action_transfer (43_action_transfer.json).
"""


class RHHiddenNodes:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pwd": ("STRING", {"default": ""}),
                "image_1": ("IMAGE",),
                "width_2": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height_3": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "image_4": ("IMAGE",),
                "width_5": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height_6": ("INT", {"default": 512, "min": 1, "max": 8192}),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "IMAGE", "INT", "INT", "IMAGE", "IMAGE",
                    "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("p0", "IMAGE_1", "IMAGE_2", "width_3", "height_4",
                    "IMAGE_5", "IMAGE_6", "width_7", "width_8",
                    "height_9", "height_10")
    FUNCTION = "route"
    CATEGORY = "RunningHub/stub"

    def route(self, pwd, image_1, width_2, height_3, image_4, width_5, height_6):
        return (
            pwd,                # p0 — passthrough pwd
            image_1, image_4,   # IMAGE_1, IMAGE_2 — основные картинки
            width_2, height_3,  # width_3, height_4 — размеры для image_1
            image_1, image_4,   # IMAGE_5, IMAGE_6 — дубли картинок
            width_2, width_5,   # width_7, width_8 — два вариант ширины
            height_3, height_6, # height_9, height_10 — два варианта высоты
        )


NODE_CLASS_MAPPINGS = {"RHHiddenNodes": RHHiddenNodes}
NODE_DISPLAY_NAME_MAPPINGS = {"RHHiddenNodes": "RHHiddenNodes (stub)"}
