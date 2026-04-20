# ofm-nodes-mirror

Зеркало всех custom ComfyUI нод, используемых в jkhlk/comfyui-ready (boевой) и jkhlk/ofm-testbed (тестовый).

- `base/` — 46 пакетов + ComfyUI + ultimate-upscale (boевой docker)
- `testbed/` — 34 пакета (testbed docker, расширение базы)
- `extras/` — bundled проприетарные: ComfyUI_INSTARAW, KiaraPanels, stubs

Все репо склонированы на конкретных коммитах (pinned SHA). Полный список с источниками — в MANIFEST.json.


---

## Changes vs upstream

- **testbed/ComfyUI-LTXVideo/example_workflows/assets/buildings.mp4** — removed (was git-lfs pointer, not needed for runtime)
- **testbed/ComfyUI-LTXVideo/example_workflows/assets/motion_track_input.jpg** — removed (was git-lfs pointer, not needed for runtime)

