# Pacousty (still in workshop phase)

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Platform: CachyOS](https://img.shields.io/badge/platform-CachyOS%20%2B%20Hyprland-8A2BE2)

Lightweight Linux voice assistant -- workshop (Needle 2 + faster-whisper) for Python beginners.

> **License:** GPL-3.0-only -- see [LICENSE](LICENSE). Copyleft.
> Deps are permissive and compatible: `cactus-needle` (Apache-2.0) + `faster-whisper` (MIT) + `sounddevice/numpy` (BSD/MIT).
> You can distribute this workshop as GPL-3.0; keep third-party LICENSE/NOTICE files when vendoring.

## Quick start (Linux CachyOS)

See [PLAN.md](PLAN.md) for full Modules 0-7.

```bash
python3 -m venv .venv; source .venv/bin/activate
pip install cactus-needle faster-whisper sounddevice numpy
NEEDLE_TELEMETRY=0 python -m assistant.trigger --text "set volume to 30"
```

## License header

Add to new Python files:

```python
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Harvy -- VoiceAssistant Workshop
```
