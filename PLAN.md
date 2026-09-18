# Voice Assistant Workshop — PLAN.md
### Build a lightweight Linux voice assistant with Needle 2, from Python basics
### Target: CachyOS + Hyprland + Quickshell (Serpantium rice) + RTX 3050-Ti | 1 hr/week
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg) `SPDX-License-Identifier: GPL-3.0-only` — Copyright (C) 2026 Harvy — see [LICENSE](../LICENSE)

> Give this file to your opencode on Linux. Tell it: "Be my workshop mentor. Follow this PLAN.md. Teach me module by module. Don't skip ahead."

---

## 1. What we are building (in plain English)

A small program that lives quietly in the background on your Linux machine.

1. You press a shortcut, e.g. `SUPER + H` (SUPER = Windows key).
2. You speak: "set volume to 30" or "open firefox".
3. The computer records your voice (a few seconds).
4. It turns voice into text. This is called **STT** = Speech-To-Text.
5. A tiny AI called **Needle 2 by Cactus** reads the text and picks a **tool** (a Python function like `set_volume`).
6. It **shows you what it wants to do and asks for approval** (you press `y` / `n`). Nothing runs without your OK in v1.
7. If approved, it runs the action. Optionally it can talk back (that's **TTS** = Text-To-Speech, but TTS is v2, not v1).
8. If Needle is not confident, it asks a bigger **chat model** for help. Local first (Ollama on your GPU), API second (optional, e.g. Groq/OpenRouter).

Why this design:

- **Lightweight:** Needle 2 is 14 MB, uses ~28 MB RAM. STT `base.en` uses ~0.5 GB VRAM. Fits easily on your RTX 3050-Ti 4 GB laptop GPU alongside a small chat model.
- **Private / local-first:** mic -> STT -> Needle all run offline. No internet needed for v1 actions.
- **Safe:** approval gate + allowlist (a list of allowed actions). The AI cannot run random shell commands in v1.

### Big picture (data flow)

```
[SUPER+H in Hyprland]
        |
        v
  Hyprland bind -> `echo go > /tmp/voice-trigger.fifo`
        |
        v
  daemon.py (already running, models already loaded)
        |
        v
  recorder.py (PipeWire mic -> .wav, 3-8 sec)
        |
        v
  stt.py (faster-whisper base.en -> "set volume to 30")
        |
        v
  brain.py (Needle 2 -> {tool: "set_volume", args: {level: 30}, confidence: 0.92})
        |
        +-- confidence high --> approver.py ("Run set_volume(30)? [y/n]") --> tools.py runs it
        |
        +-- confidence low ---> chat_fallback.py (Ollama qwen2.5:1b local, or API) --> text answer
```

**Jargon cheat-sheet (we will reuse these words):**

- **Distro:** your Linux flavor. Yours = CachyOS (based on Arch Linux, fast, rolling updates).
- **Compositor / DE:** the thing that draws windows. Yours = Hyprland (a tiling Wayland compositor, keyboard-driven, very customizable).
- **Wayland:** the new display system on Linux (replaces X11). Matters because old tricks like `xdotool` don't work. We use Hyprland-native binds.
- **Quickshell:** the tool your rice uses to draw the bar, launcher, popups in QML. We will use it in the last module for a pretty approval popup. v1 uses terminal + notifications.
- **PipeWire:** the audio system on CachyOS. It connects mic -> our program -> speakers. We check it with `wpctl` / `pactl`.
- **Daemon:** a background process that starts once and sleeps until woken. Ours loads big models once at boot so each request is fast (~2-3 sec, not 20 sec).
- **FIFO:** a special file that acts like a pipe. Writing `go` into it wakes the daemon. Path: `~/.cache/jarvis/trigger.fifo` or `/tmp/voice-trigger.fifo`.
- **systemd --user:** Linux's service manager for your user. It auto-starts our daemon on login and restarts it if it crashes.
- **venv:** virtual environment, an isolated Python folder so packages don't fight each other. We always use one.
- **STT / TTS:** Speech-To-Text (you talk -> text), Text-To-Speech (text -> robot voice).
- **Tool calling:** the AI doesn't do things directly. It outputs structured JSON like `{"name":"set_volume","arguments":{"level":30}}`, and *our Python code* runs the real function. This is safer and testable.
- **Confidence gate:** Needle returns a number 0-1 for "how sure am I". Above threshold (e.g. 0.7) we propose the action. Below -> ask chat model or ask you to repeat.
- **VRAM:** memory on your GPU. You have ~4 GB. Whisper small = ~1 GB, base = ~0.5 GB, qwen 1.5B Q4 = ~1 GB. We must stay under budget.

---

## 2. Where to build: Linux, not Windows

**Build on your CachyOS machine.** Use Windows only for reading docs and practicing Python syntax.

Reason: hotkey + audio + daemon + GPU driver stack are completely different. Code written for Windows (`global-hotkeys`, `xdotool`, Task Scheduler) gets thrown away. Hyprland binds + PipeWire + `systemd --user` only exist on Linux.

WSL2 is not recommended for this project (mic + global hotkey passthrough pain).

---

## 3. Time estimate (honest, 1 hr/week, beginner)

You can write loops/functions but aren't fluent yet. That's fine — this workshop teaches fluency by building.

| Module | What | Time |
|---|---|---|
| 0 | Python + Linux basics refresher | 4-6 hrs |
| 1 | Project skeleton + mic test on PipeWire | 3-4 hrs |
| 2 | Recorder + STT (faster-whisper) | 4-6 hrs |
| 3 | Needle 2 brain + your first 3 tools | 5-7 hrs |
| 4 | Hyprland hotkey + daemon + systemd | 4-5 hrs |
| 5 | Approval gate + safety + logs | 4-5 hrs |
| 6 | Chat fallback (Ollama local, API optional) | 4-6 hrs |
| 7 | Quickshell popup skin (Serpantium style) + polish | 4-6 hrs |
| **Total** | | **~28-39 hrs = 7-9 months at 1 hr/week** |

If you can do 2 hrs some weeks: ~4 months. v1 = modules 0-5 (no TTS, no Quickshell required). Ship v1 first. Everything after is v2.

If a module takes 2 sessions, that's normal. PipeWire + Wayland debugging is where beginners lose time. The plan accounts for it.

---

## 4. How Needle 2 works (taught like you're new)

**One-sentence version:** Needle reads your tool descriptions and your sentence, then returns JSON saying which tool to call and with what arguments.

**Slightly deeper (what your mentor must explain with a live demo):**

1. You declare tools as normal Python functions with type hints + docstring. The docstring *is* the AI's instruction. Good descriptions = good picks. This is "the whole game" per Cactus docs.
2. Example:

```python
import needle

@needle.tool
def get_weather(city: str):
    """Get the current weather for a city."""
    return {"city": city, "temp_c": 27, "sky": "clear"}

agent = needle.Needle(tools=[get_weather])
print(agent.run("what's it like in Lagos right now?")["results"])
# [{'city': 'Lagos', 'temp_c': 27, 'sky': 'clear'}]
```

3. Under the hood: Needle is a 45M-parameter model (tiny — normal chat models are 1000x bigger), compressed to ~2 bits per weight (called **CQ2 / Cactus Quants**), baked into a 14 MB engine. It uses a **byte-level grammar** — meaning it is *forced* to output valid JSON matching your tool schemas. It can't hallucinate a new tool name.
4. Key Needle features we use:
   - **Bounded memory:** 256-token sliding window, tools pinned. RAM stays ~28 MB forever. Good for a daemon.
   - **Tool retrieval:** you can declare many tools, it only considers top-5 per turn.
   - **Confidence head:** every answer has a score. We set a threshold (start 0.70). Below -> escalate to chat model.
   - **System facts (optional):** date, locale, device — passed as facts, not instructions.
5. Rules from Cactus we follow: **<=5 tools per agent, closed sets as enums (`Literal`), bounded numbers, verbatim copy for free text.** Keep tool descriptions short and distinct.
6. Install: `pip install cactus-needle`. Engine downloads once from HuggingFace and caches. Offline OK after that. Telemetry off: `NEEDLE_TELEMETRY=0`.

Your mentor must run `needle playground` with you once so you see tool-calling visually before coding.

---

## 5. How everything else works (mentor explains each with a tiny runnable)

- **Mic (PipeWire):** `wpctl status` / `pactl info | grep "Default Source"`. Python `sounddevice` records mono 16 kHz WAV. 16 kHz = enough for voice, small files. Mentor shows you how to list devices and pick the right mic.
- **STT (faster-whisper):** Whisper turns WAV -> text. `faster-whisper` is a fast version using CTranslate2. Start `base.en` (fast, English-only, small). Upgrade to `small.en` only if accuracy bad. GPU FP16 on your 3050-Ti. CPU fallback = `tiny.en` int8.
- **Hyprland bind:** in `hyprland.conf`: `bind = SUPER, H, exec, echo go > /tmp/voice-trigger.fifo`. Hyprland handles global keys natively — no extra permission group needed (unlike evdev approach).
- **Daemon + FIFO + systemd:** daemon loads STT + Needle once, then blocks reading FIFO. Trigger wakes one cycle: record -> transcribe -> reason -> propose. `systemd --user enable --now voice-assistant` starts it on login.
- **Approval:** terminal `[y/n]` + `notify-send "Voice" "Propose set_volume(30)?"` for v1. Quickshell QML card for v2 (record dot + tool + args + Approve/Deny buttons, styled to Serpantium).
- **Chat fallback:** Ollama `qwen2.5:1b-instruct` or `llama3.2:1b` Q4 (~1 GB). If Needle confidence < 0.70, ask chat model for a text answer. API (Groq/OpenRouter) is optional, key in `~/.config/voice-assistant/.env` chmod 600, never committed.
- **Safety:** allowlist only. No raw `os.system(user_text)`. Every tool logs to `~/.local/state/voice-assistant/actions.log`. Deny-by-default.

---

## 6. Repo layout (create on Linux)

```
voice-assistant/
  LICENSE               # GPL-3.0-only -- your code. Deps: cactus-needle Apache-2.0 + faster-whisper MIT (compatible with GPL-3.0, keep their NOTICE)
  pyproject.toml        # deps: cactus-needle, faster-whisper, sounddevice, numpy; license = "GPL-3.0-only"
  README.md             # how to install + use
  assistant/
    __init__.py
    daemon.py           # loads models once, waits on FIFO
    trigger.py          # `echo go` helper / --text debug mode
    recorder.py         # mic -> wav
    stt.py              # whisper -> text
    brain.py            # Needle agent + tools registry
    tools.py            # get_weather, open_app, set_volume (v1 only these 3)
    approver.py         # terminal + notify-send approve
    chat_fallback.py    # ollama / api
    config.py           # paths, thresholds, model names
  systemd/
    voice-assistant.service
  hypr/
    binds.conf.snippet  # one bind line to include
  quickshell/           # v2 only
  tests/
    test_tools.py
    test_brain_confidence.py
```

v1 tools (frozen until v1 ships — prevents scope creep):

1. `get_weather(city: str)` — returns fake-or-real weather (start fake, then wttr.in).
2. `open_app(name: Literal["firefox","kitty","nautilus"])` — launches via `hyprctl dispatch exec` / `xdg-open`. Closed enum = safe.
3. `set_volume(level: int 0-100)` — runs `wpctl set-volume @DEFAULT_AUDIO_SINK@ <level>%`. Bounded int = safe.

---

## 7. Workshop modules (mentor: do in order, one at a time)

### Module 0 — Python + Linux survival (4-6 hrs)
**Learn:** terminal basics (`ls, cd, pwd`), `python3 -m venv .venv; source .venv/bin/activate`, `pip install`, running `python file.py`, functions, dicts, JSON, `if __name__ == "__main__"`, reading errors (tracebacks).
**Do:** create `voice-assistant/`, venv, `pip install cactus-needle`, run the Lagos weather example above. Run `needle playground` once.
**Accept:** you can explain in your own words: venv, pip, function, docstring, JSON.
**Challenge:** add a 4th toy tool `add(a: int, b: int)` and call it via Needle.

### Module 1 — Mic check (3-4 hrs)
**Learn:** what PipeWire is, default source/sink, sample rate, WAV.
**Do:** `wpctl status`, `pactl info | grep "Default Source"`, record 5 sec with `pw-record` or Python sounddevice, play back, print duration + level meter.
**Accept:** a `recorder.py` that saves `test.wav` and you can hear yourself clearly.
**Troubleshoot:** wrong mic -> list devices, `pactl set-default-source <name>`; too quiet -> `alsamixer` / `wpctl set-volume @DEFAULT_AUDIO_SOURCE@`.

### Module 2 — Voice to text (4-6 hrs)
**Learn:** what STT is, model sizes (tiny/base/small), VRAM vs accuracy tradeoff, what "faster-whisper" means.
**Do:** `pip install faster-whisper sounddevice numpy`, transcribe `test.wav` with `base.en`, print text + time taken. Try `small.en` once, compare speed.
**Accept:** speak "set volume to thirty" -> text contains "volume" + "thirty/30" 3/5 tries in a quiet room.
**Challenge:** auto-stop on silence (simple energy threshold) instead of fixed 5 sec.

### Module 3 — Needle brain (5-7 hrs) — the core lesson
**Learn:** tool calling, docstrings as prompts, JSON schemas, confidence, why <=5 tools, enums/bounds.
**Do:** build `tools.py` (3 tools above) + `brain.py` (`Needle(tools=[...])`). Test with *typed* sentences first (`assistant/brain.py --text "set volume to 30"`), then with real STT output.
**Accept:** 5/5 typed tests route correctly; STT -> brain works end-to-end in terminal (no hotkey yet). Log confidence each run.
**Challenge:** deliberately write a bad vague docstring, watch accuracy drop, then fix it. This teaches prompt design.

### Module 4 — Hotkey + daemon (4-5 hrs)
**Learn:** daemon, FIFO, Hyprland bind, systemd user service.
**Do:** `daemon.py` (load once, loop on FIFO), `trigger.py`, Hyprland snippet `bind = SUPER, H, exec, echo go > /tmp/voice-trigger.fifo`, test `uv run python -m assistant.trigger --text "open firefox"`. Then create `systemd/voice-assistant.service`, `systemctl --user enable --now`.
**Accept:** press SUPER+H anywhere -> daemon wakes, records, prints transcription. Survives reboot.
**Troubleshoot:** FIFO missing -> daemon recreates; service failed -> `journalctl --user -u voice-assistant -f`.

### Module 5 — Approval + safety (4-5 hrs) — required before real actions
**Learn:** allowlist, deny-by-default, audit log, why AI never runs raw shell.
**Do:** `approver.py`: show `tool(args)` + confidence + transcription, `notify-send`, terminal `y/n`, log to `actions.log`. Wire: STT -> Needle -> approver -> tools.
**Accept:** you can demo: speak -> see proposal -> approve -> volume actually changes; deny -> nothing happens + logged. No code path runs a tool without approval in v1.
**Challenge:** add `--dry-run` flag that prints what *would* run.

### Module 6 — Chat fallback (4-6 hrs)
**Learn:** when to escalate (confidence < 0.70), local vs API models, API keys hygiene.
**Do:** install Ollama, `ollama pull qwen2.5:1b-instruct`, `chat_fallback.py`. If Needle low-confidence or no tool matches ("what's the capital of France?") -> chat answers as text (+ notify). API optional via `.env`.
**Accept:** "set volume to 30" -> tool path; "tell me a joke" -> chat path. VRAM check: `nvidia-smi` stays < 3.5 GB during both.
**Challenge:** tune threshold 0.6 vs 0.75, note false positives.

### Module 7 — Quickshell skin + polish (4-6 hrs, v2)
**Learn:** QML basics, Quickshell popup, matching Serpantium theme.
**Do:** recording dot + approval card (tool, args, confidence, Approve/Deny). Keep terminal approver as fallback.
**Accept:** full loop without opening terminal. README + `install.sh` works on fresh CachyOS login.
**Final demo:** record 60-sec video: trigger -> speak 3 commands (1 approved, 1 denied, 1 chat fallback).

---

## 8. How your mentor (opencode) must teach you

These are orders for the AI on Linux:

1. **Assume zero.** Every new tech word gets a 1-sentence plain explanation + why we need it. No unexplained jargon.
2. **One module at a time.** Never dump the whole app. Each reply: 1 concept -> 1 tiny runnable file/change -> run it -> explain output.
3. **Explain before code.** Say what will happen, then show the code, then run, then explain what happened.
4. **Small diffs.** Max ~50 lines of new code per step. If more needed, split.
5. **You type and run.** Mentor gives commands for *you* to paste. It doesn't pretend to hear your mic — it asks you to paste output back.
6. **Check understanding.** End each step with 1-2 questions ("in your own words, what does FIFO do?"). Wait for answer before continuing.
7. **Fix errors together.** On traceback: read last line first, explain cause simply, fix one thing, re-run.
8. **No secrets in repo.** `.env` stays in `~/.config/`, `chmod 600`, listed in `.gitignore`.
9. **Log progress.** After each session, append to `PROGRESS.md`: date, what worked, time taken, next step.

Starter prompt to paste into Linux opencode:

> "Be my workshop mentor. Follow PLAN.md strictly. I am a Python beginner, not a tech person — explain every tech word simply but use the correct term too. Go module by module starting at Module 0. One small step at a time. Ask me to run commands and paste output. Don't write the whole app at once. After each session update PROGRESS.md."

---

## 9. Changing the plan (allowed, but controlled)

You asked for flexibility — here's the rule so we don't derail:

- **Minor change** (swap `base.en` -> `small.en`, change shortcut, add 1 tool): just say so. Mentor updates PLAN.md's "Decisions log" below and continues. Max 5 tools still holds for Needle accuracy.
- **Medium change** (add TTS early, switch chat model, change overlay design): finish the current module first, then mentor proposes new acceptance test + time cost before changing.
- **Major change** (new OS, new AI, "also control smart home"): pause, write a 5-line proposal (goal / why / cost / risk / test), approve explicitly, then update plan.
- Mentor must never silently expand scope. If you say "can it also...?", it answers: "Yes, that's Module X / v2. Finish current acceptance first?"

### Decisions log (mentor appends here)
- [2026-09-12] Initial plan: v1 = STT + Needle + approval, no TTS. STT = base.en. Threshold 0.70. Shortcut SUPER+H. (Change/add below.)
- [2026-09-18] License: GPL-3.0-only (Copyright C 2026 Harvy). Copyleft chosen; no hosting need so not AGPL. Compatible with deps: cactus-needle Apache-2.0 + faster-whisper MIT are GPL-3.0 compatible (Apache-2.0 NOT compatible with GPL-2.0 only). When you create `pyproject.toml`, set `license = "GPL-3.0-only"` and `classifiers = ["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"]`, keep third-party LICENSE/NOTICE when vendoring, add `SPDX-License-Identifier: GPL-3.0-only` header to new `.py` files.

---

## 10. CachyOS quick reference (for mentor)

```bash
# env
python3 -m venv .venv; source .venv/bin/activate
pip install cactus-needle faster-whisper sounddevice numpy
export NEEDLE_TELEMETRY=0

# audio
wpctl status
pactl info | grep "Default Source"
pw-record --channels 1 --rate 16000 test.wav  # ctrl+C to stop

# gpu
nvidia-smi

# hyprland (add to hyprland.conf or include snippet)
# bind = SUPER, H, exec, echo go > /tmp/voice-trigger.fifo

# daemon test without hotkey
python -m assistant.trigger --text "set volume to 30"

# service
systemctl --user enable --now voice-assistant
journalctl --user -u voice-assistant -f

# notify
notify-send "Voice" "Propose set_volume(30)?"
```

`voice-assistant.service` template:

```ini
[Unit]
Description=Voice assistant daemon
After=pipewire.service

[Service]
ExecStart=%h/voice-assistant/.venv/bin/python -m assistant.daemon
Restart=on-failure
Environment=NEEDLE_TELEMETRY=0

[Install]
WantedBy=default.target
```

`pyproject.toml` license snippet (add when you create the file on Linux):

```toml
[project]
name = "voice-assistant"
license = {text = "GPL-3.0-only"}
classifiers = ["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"]
# keep deps permissive: cactus-needle (Apache-2.0) + faster-whisper (MIT) are GPL-3.0 compatible
```

Add to top of every new `assistant/*.py` :

```python
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Harvy
```

---

## 11. Definition of done (v1 ships when...)

- [ ] SUPER+H works from any app on Hyprland
- [ ] 3 tools work via voice + approval 4/5 tries in quiet room
- [ ] Deny path tested + logged
- [ ] Low-confidence -> chat fallback tested
- [ ] Survives reboot (systemd)
- [ ] README install steps verified
- [ ] No API key in repo, no tool runs without approval

Then celebrate, then start v2 (TTS with Piper, Quickshell card, 4th/5th tool).

Good luck — slow is smooth, smooth is fast. One hour a week still ships if we keep scope tight.
