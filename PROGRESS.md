# PROGRESS — voice-assistant workshop sessions

> Mentor: append one entry per session. User: paste last entry back if switching machines.
> Format: date, minutes spent, module, what worked, what didn't, next step.

---

## Sessions (newest at bottom)

### YYYY-MM-DD — Module _ — _ min
- **Did:**
- **Worked:**
- **Didn't / errors seen (paste last lines):**
- **Understood (in my own words):**
- **Next:**

### 2026-09-14 — Module 0 Part 1 (WSL) — short session
- **Did:** created `.venv`, activated it, `pip install cactus-needle`, verified with `python -c "import needle; print('needle ok')"` → `needle ok`.
- **Worked:** venv shows `(.venv)` prefix; install + import clean, no errors.
- **Didn't / errors seen (paste last lines):** none.
- **Understood (in my own words):** venv = isolated Python folder (like the Docker idea but Python-only); the `(.venv)` prompt prefix means the shell is using the venv.
- **Next:** Module 0 Part 2 — first Needle tools (`toy.py`).

### 2026-09-14 — Module 0 Parts 2-3 (WSL) — ~90 min total
- **Did:** fixed `huggingface_hub` (0.0.18→upgrade, `ValueError: Invalid repo type`), ran `toy.py` (`add` + `get_weather` → `listing(dir)`), docstring break experiment (`"Do stuff."` → `[]` both lines), vocab test (`"what is 4+5?"` → `[]`, `"add 4 and 5"` → `[{'result':9}]`), `listing("./")` + pretty `json.dumps`, `IndexError` guard (`if out:`), `practice_errors.py` (`set_volume` + `open_app` allowlist with `raise ValueError` + `try`/`except`).
- **Worked:** Needle picks + executes tools, `json.dumps` dict→str understood, `raise`→`except` flow, allowlist `{"firefox","kitty","nautilus"}` — `open_app("firefox")` → `{"app":"firefox"}`, `open_app("chrome")` caught.
- **Didn't / errors seen (paste last lines):** `huggingface_hub ValueError`, vague docstring broke both tools (surprised prediction), `IndexError: list index out of range` on empty `out[0]` — both fixed by one-change tests.
- **Understood (in my own words):** Needle = matches tool description + fills args → runs our function → returns our dict; model JSON is forced by grammar, our function should return dict; outer `[]` = one slot per tool call; `json.dumps`/`loads` = dict↔str; `raise` creates error now, `try`/`except` catches it; last traceback line = cause.
- **Next:** Module 1 mic check — needs real CachyOS Linux (PipeWire `wpctl`/`pactl` + `sounddevice`); WSL pause. Bring `PLAN.md` + `AGENTS.md` + `PROGRESS.md` to Linux and paste AGENTS.md Role prompt.

### 2026-09-21 — Module 1 (CachyOS) — ~45 min
- **Did:** `wpctl status` + `pactl info` (source `alsa_input...analog-stereo` 0.27, sink 0.00 muted), `timeout 5 pw-record test.wav` (156K mono 16kHz 5.0s verified), unmuted sink → 50% + `pw-play` ok, skeleton `voice-assistant/assistant/` + `__init__.py` + `.venv` + `sounddevice numpy` clean, `recorder.py` (rec + peak + first-10 + loudness bar) → `test_py.wav` peak ~11k, first-10 zeros (spoke late), playback audible but noisy.
- **Worked:** record/save/play via CLI + Python; source=input/sink=output understood; sample rate (16000×5=80000) + abs/peak taught via fake 5-sample demo.
- **Didn't / errors seen (paste last lines):** background loud (no BT earphones, abandoned after 2h debug); first-10 zeros (timing, not bug); sink started muted at 0.00.
- **Understood (in my own words):** source is input, sink is output; 16000 = snapshots/sec; peak = loudest abs sample; `sd.wait()` blocks until done.
- **Next:** Module 2 STT — faster-whisper `base.en` transcribes test_py.wav.

### 2026-09-23 — Module 2 STT (CachyOS) — ~40 min
- **Did:** `pip install faster-whisper` + `stt.py` (base.en, cuda, float16); taught argv/time/segments/join + epoch demo + float32-vs-16 demo; fixed `:.f`→`:.1f`; fixed `libcublas.so.12` via `pip install nvidia-cublas-cu12` (NOT system cuda 13.4 = wrong .so.13) + `LD_LIBRARY_PATH`; persisted export in `.venv/bin/activate`.
- **Worked:** `Loaded 1.8–6.7s, transcribe 0.5–0.6s, lang=en p=1.00`; acceptance `"Set volume to 30. Set volume to 30."` PASS 1/1.
- **Didn't / errors seen (paste last lines):** `ValueError: Format specifier missing precision` (typo, fixed); `RuntimeError: libcublas.so.12 not found` at encode only (load fine — fixed by export); counting clip hallucinated `"Thank you so much. Have a nice day."` (noise, predictor filler).
- **Understood (in my own words):** epoch = 1970 zero line, subtract for stopwatch; float16 = half bytes, nets don't care; segments joined; .so.12 vs .so.13 must match; LD_LIBRARY_PATH = lib address book.
- **Next:** Module 3 brain — `tools.py` (3 frozen tools) + `brain.py` typed tests, then live STT text.

<!-- Example:
### 2026-09-14 — Module 0 — 60 min
- **Did:** venv + pip install cactus-needle, ran Lagos weather example.
- **Worked:** tool ran, results printed.
- **Didn't / errors:** none.
- **Understood:** venv is an isolated Python folder so packages don't clash.
- **Next:** WINDOWS_PRACTICE Part 2 / Module 1 mic check on Linux.
-->
