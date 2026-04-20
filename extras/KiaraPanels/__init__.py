"""KiaraPanels stub — для kiara_sasat.json + animator_v25.json.

Оригинальный пакет приватный (не найден на GitHub). Реконструирован из workflow signatures.

4 класса:
- KiaraReferenceLatent: обёртка над core ReferenceLatent (reference_latents set)
- ControlPanelFlux: aspect_ratio + steps_preset → (width, height, steps)
- ControlPanelSD: aspect_ratio + steps_preset + cfg → (width, height, steps, cfg)
- FancyTimerNode: UI-only таймер (pass-through заглушка)
"""


# Пресеты aspect ratio для Flux/SDXL — стандартные значения
_ASPECT_RATIOS = {
    '1:1 Square 1024x1024': (1024, 1024),
    '2:3 Portrait 832x1216': (832, 1216),
    '3:4 Portrait 896x1216': (896, 1216),
    '3:4 Portrait 896x1152': (896, 1152),
    '9:16 Tall 768x1344': (768, 1344),
    '9:16 Tall 832x1472': (832, 1472),
    '9:16 Tall 896x1536': (896, 1536),
    '9:21 Tall 640x1536': (640, 1536),
    '4:3 Landscape 1216x896': (1216, 896),
    '3:2 Landscape 1216x832': (1216, 832),
    '16:9 Landscape 1344x768': (1344, 768),
    '16:9 Landscape 1472x832': (1472, 832),
    '16:9 Landscape 1536x896': (1536, 896),
    '21:9 Wide 1536x640': (1536, 640),
}

_SPEED_PRESETS = {
    'Fast 4 steps': 4,
    'Fast 6 steps': 6,
    'Fast 8 steps': 8,
    'Quality 12 steps': 12,
    'Quality 20 steps': 20,
    'Quality 30 steps': 30,
}


class KiaraReferenceLatent:
    """Копия core ReferenceLatent — вписывает reference_latents в conditioning."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "latent": ("LATENT",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "apply"
    CATEGORY = "KiaraPanels"

    def apply(self, conditioning, latent):
        import node_helpers
        out = node_helpers.conditioning_set_values(
            conditioning, {"reference_latents": [latent["samples"]]}, append=True
        )
        return (out,)


class ControlPanelFlux:
    """Hub-нода для Flux: aspect + speed → (width, height, steps)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (list(_ASPECT_RATIOS.keys()), {"default": "9:16 Tall 896x1536"}),
                "speed_preset": (list(_SPEED_PRESETS.keys()), {"default": "Fast 4 steps"}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "steps")
    FUNCTION = "run"
    CATEGORY = "KiaraPanels"

    def run(self, aspect_ratio, speed_preset):
        w, h = _ASPECT_RATIOS.get(aspect_ratio, (896, 1536))
        steps = _SPEED_PRESETS.get(speed_preset, 4)
        return (w, h, steps)


class ControlPanelSD:
    """Hub-нода для SDXL: aspect + speed + cfg → (width, height, steps, cfg)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (list(_ASPECT_RATIOS.keys()), {"default": "9:16 Tall 896x1536"}),
                "speed_preset": (list(_SPEED_PRESETS.keys()), {"default": "Fast 8 steps"}),
                "cfg": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 30.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "FLOAT")
    RETURN_NAMES = ("width", "height", "steps", "cfg")
    FUNCTION = "run"
    CATEGORY = "KiaraPanels"

    def run(self, aspect_ratio, speed_preset, cfg):
        w, h = _ASPECT_RATIOS.get(aspect_ratio, (896, 1536))
        steps = _SPEED_PRESETS.get(speed_preset, 8)
        return (w, h, steps, float(cfg))


class FancyTimerNode:
    """UI-only таймер. Stub не выполняет никакой работы — только чтобы
    class_type в workflow JSON матчился на registered node."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "label": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "noop"
    CATEGORY = "KiaraPanels"
    OUTPUT_NODE = True

    def noop(self, label):
        return {}


NODE_CLASS_MAPPINGS = {
    "KiaraReferenceLatent": KiaraReferenceLatent,
    "ControlPanelFlux": ControlPanelFlux,
    "ControlPanelSD": ControlPanelSD,
    "FancyTimerNode": FancyTimerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KiaraReferenceLatent": "Kiara Reference Latent (stub)",
    "ControlPanelFlux": "Kiara Control Panel Flux (stub)",
    "ControlPanelSD": "Kiara Control Panel SD (stub)",
    "FancyTimerNode": "Fancy Timer (stub)",
}
