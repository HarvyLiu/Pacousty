# HANDOFF / LOG — voice-assistant workshop

> **Purpose:** continue anywhere (Windows opencode, Linux opencode, new chat) without missing anything.
> **Rule for AI:** after EVERY reply/conversation, append a new entry to `## Log` below (date, what user asked, what you did, decisions, next step). Keep it detailed but factual. Never delete old entries.

---

## 1. Current status (update this block each time)

- **Date:** 2026-09-21
- **Phase:** Module 0 DONE. On CachyOS Linux (confirmed). Side-quest in progress: Stardance + Hackatime + Neovim hour tracking. Next = verify Hackatime heartbeat, then Module 1 mic check.
- **Files:** `PLAN.md` ✅, `HANDOFF.md` ✅, `PROGRESS.md` ✅ (2 entries), `WINDOWS_PRACTICE.md` ✅, `AGENTS.md` ✅. Nvim: `~/.config/nvim/init.lua` + vim-wakatime (added 2026-09-21 with ==== opencode banner). No `~/.wakatime.cfg` yet (user must run hackatime setup page).
- **Next step for user:** 1) visit hackatime.hackclub.com/setup while logged in, 2) restart nvim, code 2-3 min in workshop repo, 3) paste verify outputs back. Then link Hackatime project on Stardance project page + devlog.
- **Blocking questions:** none. Open detail: exact Serpantium rice repo URL (not needed until Module 7).

## 2. Context (who / what / where)

- **User:** Python beginner. Can write basic loops/functions but "sucks", not fluent writing, good at reading/watching code. Wants to be treated as non-tech: use correct tech words BUT explain each simply. Wants real skills, not just copy-paste.
- **Goal:** lightweight Linux background voice assistant. Press shortcut → speak → transcribe → Needle 2 picks tool → **asks approval** → runs local action + optional chat reply. Chat model = local-first (Ollama), API optional.
- **Target machine:** CachyOS + Hyprland + Quickshell (Serpantium rice). GPU: RTX 3050-Ti laptop (~4 GB VRAM). Mic via PipeWire.
- **Time budget:** ~1 hr/week. Estimate 28-39 hrs total → 7-9 months calendar. v1 = Modules 0-5 (no TTS, no Quickshell required).
- **Build OS decision:** BUILD ON LINUX (CachyOS). Windows only for Python syntax practice. WSL2 not recommended (mic + global hotkey pain).

## 3. Key technical findings (don't re-research unless stuck)

- **Needle 2 (cactus-compute/needle):** 45M-param tool-calling model, 14 MB binary, ~28 MB RAM session, CQ2-bit (Cactus Quants trained from start, not post-quantized). `pip install cactus-needle`. Pattern: `@needle.tool` + `Needle(tools=[...])` + `agent.run(text)["results"]`. Byte-level grammar forces valid JSON. Features: confidence score per reply (we gate at 0.70), tool retrieval (top-5), bounded 256-token window. Rules: ≤5 tools, closed sets as `Literal`, bounded ints, good docstrings = accuracy. Engine downloads once from HF, then offline. `NEEDLE_TELEMETRY=0`. Playground: `needle playground`.
- **STT:** `faster-whisper` (CTranslate2). Start `base.en` (~0.5 GB VRAM, ~140 ms first-segment on 3050-class). `small.en` (~1 GB, ~380 ms) if accuracy needs it. 3050-Ti 4 GB can hold base/small + qwen 1-1.5B Q4 (~1 GB) together. Record mono 16 kHz WAV via `sounddevice` on PipeWire default source (`wpctl status`, `pactl info | grep "Default Source"`).
- **Trigger/daemon (Hyprland Wayland):** no `global-hotkeys`/`xdotool`/`evdev` needed for v1. Use Hyprland native: `bind = SUPER, H, exec, echo go > /tmp/voice-trigger.fifo`. Daemon loads models once, blocks on FIFO, one cycle per trigger. Same pattern as Jarvis (`mraull1108/AI-Local-Assistant`). `systemd --user` service for autostart (see `PLAN.md §10` template).
- **Approval/safety:** allowlist only (v1: `get_weather`, `open_app` with Literal enum, `set_volume` 0-100). Deny-by-default, no raw shell from model text, log to `actions.log`. v1 approver = terminal y/n + `notify-send`; v2 = Quickshell QML card styled to Serpantium.
- **Chat fallback:** Ollama `qwen2.5:1b-instruct` or `llama3.2:1b` Q4 local-first; API (Groq/OpenRouter) optional via `~/.config/.../.env` chmod 600, never committed.
- **Serpantium rice:** exact repo not found in search (found similar CachyOS+Hyprland+Quickshell rices like sea-shell, caelestia). Doesn't block v1. Needed only in Module 7 for skinning.

## 4. Decisions made

1. Scope v1 = voice tool-doer WITH approval, no TTS. (user confirmed)
2. STT start = `base.en`, threshold 0.70, shortcut SUPER+H. (in PLAN Decisions log 2026-09-12)
3. Teaching style = mentor mode, one module at a time, ≤50 lines/step, explain-before-code, user runs commands, check understanding, log to PROGRESS.md. (PLAN §8)
4. Plan changes allowed but controlled: minor anytime, medium after current module + cost note, major needs 5-line proposal. (PLAN §9)
5. Extra files requested: this HANDOFF/LOG + PROGRESS template + Windows practice sheet. (2026-09-12)
6. `AGENTS.md` created as portable mentor instructions (role prompt + teaching rules + safety + bookkeeping + machine notes) so any AI anywhere teaches the same way. (2026-09-12)

## 5. Files inventory

| File | What |
|---|---|
| `PLAN.md` | Workshop plan, Modules 0-7, mentor rules, CachyOS ref, done checklist |
| `HANDOFF.md` | This file — status + context + full conversation log |
| `PROGRESS.md` | Per-session log (mentor appends after each session) |
| `WINDOWS_PRACTICE.md` | Windows-safe Module 0 practice (no mic/hotkey needed) |
| `AGENTS.md` | Portable mentor instructions + role prompt (drop next to PLAN.md or paste anywhere) |

## 6. How to resume (for any AI or user)

1. Read this file top-to-bottom, then `PLAN.md`, then last entries of `PROGRESS.md` + `## Log` below.
2. Continue from `## 1. Current status → Next step`.
3. After your reply, append to `## Log` and update `## 1` if status changed. Also append to `PROGRESS.md` if a session happened.

---

## Log (append-only — newest at bottom)

### 2026-09-12 — Session 1: goal + Windows-vs-Linux + estimate (Windows opencode)
- **User asked:** build workshop with AI teacher; Windows or Linux? Only 1 hr/week on Linux — how long? Plan first, write PLAN.md for Linux opencode to mentor from Python basics. Project: lightweight Linux background process with Needle AI, shortcut summon, voice commands, Needle2-by-Cactus wired to chat model (local-first/API).
- **Assistant did:** researched cactus-compute/needle (Needle 2 specs), Linux hotkey/voice patterns (Hyprland binds, faster-whisper-hotkey, Jarvis FIFO+systemd, LinuxWhisper), asked 4 clarifying Qs (distro/DE, hardware, Python level, v1 scope).
- **User answered:** CachyOS + Hyprland + Serpantium/Quickshell rice; RTX 3050-Ti; Python beginner (loops/functions shaky, reads well); scope = voice tool-doer with approval gate.
- **Assistant did:** researched Hyprland binds, faster-whisper VRAM/latency on 3050-class, CachyOS/Hyprland/Quickshell rices. Gave verdict (build on Linux), estimate table (28-38 h → 7-9 mo at 1 h/wk), PLAN.md draft outline. Noted plan-mode read-only, asked approval to write file.
- **Outcome:** user approved direction.

### 2026-09-12 — Session 2: teaching style + PLAN.md written (Windows opencode)
- **User asked:** teach everything in process, allow minor plan changes, explain Needle + everything as if non-tech (use tech words + explain them), want real skills, write PLAN.md.
- **Assistant did:** read `opencode.json`, checked no PLAN*.md existed, wrote `PLAN.md` (goal, architecture diagram, jargon sheet, Needle explainer, Modules 0-7 with Learn/Do/Accept/Challenge, mentor rules + starter prompt, change protocol + Decisions log, CachyOS ref + systemd template, done checklist). Offered PROGRESS template / Windows practice sheet.
- **Outcome:** PLAN.md created. User said "yeah sure" + requested HANDOFF/LOG md.

### 2026-09-12 — Session 3: HANDOFF + templates (Windows opencode, build mode)
- **User asked:** "yeah sure" (to PROGRESS template + Windows practice) + write HANDOFF/LOG md detailing everything after each reply so we can continue anywhere.
- **Assistant did:** created `HANDOFF.md` (this file), `PROGRESS.md` template, `WINDOWS_PRACTICE.md` (Module 0 Windows-safe exercises). Mode changed plan→build during this turn.
- **Next:** user does WINDOWS_PRACTICE Part 1, then moves to Linux with PLAN.md + PROGRESS.md.

### 2026-09-12 — Session 4: AGENTS.md (Windows opencode, build mode)
- **User asked:** write an Agents.md including the role part ("Be my workshop mentor. Follow PLAN.md strictly. I am a Python beginner — explain every tech word simply but use the correct term too. Go module by module starting at Module 0. One small step at a time.") so teaching works the same anywhere.
- **Assistant did:** wrote `AGENTS.md` (role prompt verbatim + who/constraints + first-session procedure + 6 teaching rules + safety/scope + bookkeeping + Windows/Linux machine notes). Updated this HANDOFF status/decisions/inventory.
- **Next:** user does WINDOWS_PRACTICE, then to Linux with PLAN.md + AGENTS.md + PROGRESS.md.

### 2026-09-14 — Session 5: WSL orientation + Module 0 Part 1 start (WSL opencode)
- **User asked:** read everything, follow instructions, on Windows WSL — what now? Then: yes, plus remember to write handoffs/mds.
- **Assistant did:** read HANDOFF/PLAN/PROGRESS/WINDOWS_PRACTICE, verified WSL2 (`6.6.87.2-microsoft-standard-WSL2`, Python 3.14.6). Stated Module 0 / last next step / today's single goal per AGENTS.md. Explained WSL = practice-only (no Hyprland/PipeWire/daemon build here). Started Module 0 Part 1 (WSL bash venv flow). Updated `## 1. Current status`.
- **Next:** user runs Part 1 commands, pastes output back; then debrief + PROGRESS.md entry.

### 2026-09-14 — Session 5 (cont.): Part 1 answers received, verify pending
- **User answered:** venv = Virtual Environment, keeps env same, like docker/Nyx; knows venv active via `(.venv)` prompt prefix.
- **Assistant did:** confirmed answers (venv vs Docker/Nix distinction), asked for missing evidence: output of `python -c "import needle; print('needle ok')"`.
- **Next:** user pastes verify output; then Part 2 (`toy.py`) or fix install error from last 5 lines.

### 2026-09-14 — Session 5 (cont. 2): Part 1 verified, Part 2 started
- **User reported:** `needle ok` — install + import clean.
- **Assistant did:** marked Part 1 done, wrote PROGRESS.md entry, updated status, started Part 2 (`toy.py`: `add` + `get_weather` via Needle).
- **Next:** user runs `python toy.py`, pastes output back; then docstring experiment + `greet` tool.

### 2026-09-14 — Session 5 (cont. 3): waited on toy.py output
- **User pasted:** the last 3 lines of `toy.py` source (agent + 2 print lines) — no terminal output yet.
- **Assistant did:** clarified code vs output, re-asked for terminal text after `python toy.py`.
- **Next:** user pastes what the terminal printed (or last 5 lines if error).

### 2026-09-14 — Session 5 (cont. 4): toy.py traceback diagnosed
- **Error (last line first):** `ValueError: Invalid repo type` from `huggingface_hub/file_download.py hf_hub_url`.
- **Cause:** version mismatch — `cactus-needle 2.0.14` asks for its engine with `repo_type="model"`, but pip installed ancient `huggingface-hub 0.0.18` whose `REPO_TYPES = [None, dataset, space]` (no `"model"`; models = blank). User code is fine.
- **Fix given:** `pip install --upgrade huggingface_hub`, then re-run `python toy.py`.
- **Next:** user pastes upgrade + rerun output.

### 2026-09-14 — Session 5 (cont. 5): upgrade fixed it, Needle ran with quirks
- **User pasted:** `[]` then `[{'city': 'Taipei', 'temp_c': 27, 'sky': 'clear'}]`.
- **Meaning:** fix worked (engine downloaded, tools called). Quirk 1: `[]` = Needle picked NO tool for "what is 4 + 5?". Quirk 2: asked Lagos, got `Taipei` = tiny model garbled the free-text city arg.
- **Assistant did:** explained both lines, gave next single step: docstring-break experiment (`add` docstring → `"Do stuff."`, rerun, paste, restore).
- **Next:** user pastes experiment output + answers docstring question; then `greet` tool.

### 2026-09-14 — Session 5 (cont. 6): Taipei explained, "how does Needle work" asked
- **User clarified:** they changed Lagos → Taipei themselves. Asked: where did 27°C come from — hallucination? Said docstring tells Needle what the tool does, wants under-the-hood how.
- **Assistant explained:** 27 came from THEIR code — `get_weather` is hardcoded fake (`return {"city": city, "temp_c": 27, ...}`); Needle only picked tool + city, our function supplied temp. Taught tool-calling split (AI picks JSON, code executes) + Needle internals (45M params, CQ2 14MB engine, byte-level grammar → valid JSON, confidence).
- **Next:** break experiment (`"""Do stuff."""`, rerun, paste, restore), then `greet` tool.

### 2026-09-14 — Session 5 (cont. 7): break experiment surprised us
- **User ran:** vague `add` docstring → `[]` for BOTH lines (weather broke too, not just math).
- **Lesson:** assistant's prediction (weather survives) was wrong; evidence wins. Likely cause: tiny model scores ALL tools jointly + both `agent.run` calls share one agent memory, so one bad description poisons everything. Docstrings = "the whole game" (Cactus docs).
- **Next:** restore good docstring, rerun, paste (expect both lines back); then `greet` tool.

### 2026-09-14 — Session 5 (cont. 8): screenshot — longer docstring still [], plus stray "H"
- **User showed:** even detailed `add` docstring still gives `[]` for math; weather fine. Asked about an `H` at line 4 in editor.
- **Assistant explained:** `H` = Neovim UI (sign/number column), not file content — program runs, so file is valid; verify with `sed -n '4p' toy.py`. New hypothesis: vocab match — query "what is 4 + 5?" lacks verb "add"; tiny models match words literally.
- **Next:** change query to `"add 4 and 5"`, rerun, paste both lines.

### 2026-09-14 — Session 5 (cont. 9): vocab hypothesis CONFIRMED
- **User ran:** query `"add 4 and 5"` → `[{'result': 9}]` + weather line. Earlier "what is 4 + 5?" → `[]`.
- **Lesson:** tiny model matches vocabulary literally — query must contain the docstring's verb. Directly previews Module 3 voice-command wording.
- **Next:** add third tool `greet(name)`, call via `agent.run("greet Ana")`, paste output; then Part 3.

### 2026-09-14 — Session 5 (cont. 10): user summarized tool-calling, asked about JSON
- **User said:** Needle matches tool description from prompt → runs function → outputs. Asked: what if not JSON format? Built own `listing(dir)` tool with bare `return` (screenshot).
- **Assistant explained:** model side is ALWAYS JSON (grammar-forced); our function should return dicts (JSON-like) so downstream code gets named fields; bare `return` = `None` = nothing usable in results.
- **Next:** finish `listing` body with `os.listdir`, run "list ..." query, paste output; then Part 3.

### 2026-09-14 — Session 5 (cont. 11): output nesting explained
- **User ran:** `listing` works (listed `/` once, workshop dir once — model guessed path differently per run). Asked: why output looks like `[{'contents': [...]}]` — lists vs dicts.
- **Correction (user):** paths were USER-specified (`../` vs `./` queries across runs) — not model flakiness. Assistant's guess was wrong; record fixed.
- **User asked:** why must results be a list? Answered: one slot per tool call — a turn can trigger several calls, uniform shape so code loops without special-casing.
- **Assistant explained:** outside-in: outer `[]` = results list (one slot per tool call), `{}` = our dict, `'contents'` = our key, inner `[]` = `os.listdir`'s filename list. Noted path-guess flakiness → approval-gate reason.
- **Next:** pretty-print experiment (`json.dumps` + index first file), paste output; then Part 3 errors.

### 2026-09-14 — Session 5 (cont. 12): IndexError taught
- **User ran:** pretty-print snippet with query "list the contents of ." → `[]`, then `IndexError: list index out of range` on `out[0]`.
- **Cause:** model picked no tool for that phrasing (`out` = empty), so position 0 doesn't exist. Taught: last-line-first reading + guard with `if out:` before indexing (previews confidence gate).
- **Next:** rerun with guard + earlier working phrasing, paste output; then Part 3 errors.

### 2026-09-14 — Session 5 (cont. 13): guard run done, into Part 3
- **User reported:** guard experiment done (no output pasted, trusted).
- **Assistant did:** moved to Part 3 (JSON + errors: `json.dumps`, bounded `set_volume`, `try`/`except`, `open_app` allowlist). Updated status to Part 3.
- **Next:** user runs Part 3 challenge — `open_app` allowlist — pastes output; then Module 0 wrap check.

### 2026-09-14 — Session 5 (cont. 14): Part 3 definitions answered + JSON-vs-dict confusion
- **User asked:** why `json.dumps` if we already `return {"volume": 30}` in JSON format?
- **Assistant clarified:** `return {"volume": 30}` is a Python `dict` (in RAM, single quotes when printed) — NOT JSON text. `json.dumps` → JSON text string (double quotes, the format the outside world uses). Needle/library handles the translation; we call `dumps` when we need a saveable/sendable string.
- **User answered:** `raise` sets a specified error to be called in future — close, corrected to "creates the error *right now* when the `if` is true".
- **User pasted:** `{"app": "firefox"}` / `caught: not allowed: chrome...` — `open_app` allowlist works; `except` caught the `ValueError`.
- **Next:** Module 0 wrap check (6 terms + toy tool).

### 2026-09-14 — Session 5 (cont. 15): Module 0 marked DONE
- **User confirmed:** Module 0 wrap — "log done i guess". Pasted `open_app` success output as evidence.
- **Assistant did:** logged PROGRESS.md entry for Parts 2-3 (~90 min total, all practice tasks + fixes), updated `## 1. Current status` to Module 0 DONE, noted WSL files (`toy.py`, `practice_errors.py`). Explained Module 1 requires real Linux (PipeWire `wpctl`/`pactl` + `sounddevice` not in WSL).
- **Next:** user moves to CachyOS with `PLAN.md` + `AGENTS.md` + `PROGRESS.md`, pastes Role prompt.

### 2026-09-14 — Session 5 (cont. 16): WSL toy files reuse asked
- **User asked:** will `toy.py` / `practice_errors.py` be used in Module 1?
- **Answer:** No — WSL toys stay as reference; real build on Linux creates fresh `voice-assistant/` layout per `PLAN.md §6` (`assistant/recorder.py`, `stt.py`, `tools.py`, `brain.py`, etc.) + new `.venv`. Don't copy WSL `.venv`/`toy.py` to Linux; copy only the three mds.
- **User answered:** `json.dumps` = dump whole JSON to modify; `try`/`except` = if no error do try, if error do except.
- **Assistant corrected:** `json.dumps` = dict → JSON text (a string), not modifying JSON; `json.loads` is the reverse. `try`/`except` = attempt block, on specific error (`ValueError`) jump to handler — confirmed user's core idea correct.
- **Next:** user runs JSON-vs-dict demo (`print(dict)` vs `json.dumps`), pastes output; then `open_app` challenge.

### 2026-09-21 — Session 6: CachyOS confirmed + Stardance/Hackatime/Neovim side-quest start (CachyOS opencode)
- **User asked:** read all instructions first + follow them; connect to Stardance Hack Club + record hours; uses Neovim; if editing nvim config use ==== banner with "This is added by opencode".
- **Assistant did:** read HANDOFF/PLAN/PROGRESS/README + `~/.config/nvim/init.lua` (lazy.nvim, no lua/ folder, no ~/.wakatime.cfg). Verified CachyOS rolling, nvim 0.12.5. Researched Stardance (June1-Sept30 2026, Hackatime tracks, Stardance counts on devlog) + Hackatime Neovim docs (setup page → ~/.wakatime.cfg, then wakatime/vim-wakatime, git repo required). Asked 3 Qs per AGENTS.md (goal/status/nvim-edit).
- **User answered:** goal = Stardance hours first, has Hackatime + Stardance project already, yes edit init.lua.
- **Assistant did:** added `{ "wakatime/vim-wakatime", lazy = false }` to lazy.setup with ==== opencode banner (lines ~79-85). Updated ## 1 status to 2026-09-21 CachyOS side-quest.
- **Next:** user visits hackatime.hackclub.com/setup, restarts nvim, codes 2-3 min, pastes verify outputs; then link project on Stardance page + devlog; then Module 1 mic check.

### 2026-09-21 — Session 7: Hackatime dropped, Module 1 Step 1 start (CachyOS opencode)
- **User said:** done, don't care about hackatime in workshop, start building on linux pc. Confirmed "yeah ok" to Module 1 Step 1 = 5-sec mic record only.
- **Assistant verified:** PipeWire 1.6.8, default source `alsa_input.pci-0000_06_00.6.analog-stereo` vol 0.27, sink vol 0.00, RTX 3050-Ti 4096 MiB, Python 3.14.7. No `voice-assistant/` or `.venv` on Linux yet.
- **Decision (minor, per PLAN §9):** Hackatime/Stardance hour-tracking out of workshop scope. Nvim vim-wakatime line stays (harmless) but no further tracking work. Focus = v1 Modules 1-5.
- **Next:** user runs `timeout 5 pw-record` + `ls -lh/file` verify, pastes output; then playback check + Step 2 (venv + recorder.py).

### 2026-09-21 — Session 7 (cont.): Step 1 record verified, playback pending
- **User pasted:** `test.wav` 159k (eza). Assistant verified: `156K, RIFF WAVE, 16-bit mono 16000 Hz, 5.0 sec` — math matches (16000×2 bytes×5s ≈ 156K). Sink vol 0.00 = muted, source was 0.27 earlier.
- **Next:** user unmutes sink to 50%, runs `pw-play test.wav`, confirms hearing self clearly; then Step 2 (venv + recorder.py).

### 2026-09-21 — Session 7 (cont. 2): playback ok (room tone only), vol question asked
- **User reported:** hears clearly but only environment sounds (didn't speak). Answered source=input/sink=output (correct). Asked why source is 0.27, auto?
- **Answer given:** 0.27 = 27% mic gain on 0.0-1.0 scale, persisted by WirePlumber/desktop settings, not live auto-gain; adjustable via wpctl.
- **Next:** user re-records WITH speech (count 1-5), plays back, pastes output; then Step 2 (venv + recorder.py).

### 2026-09-21 — Session 7 (cont. 3): Step 1 accepted, Step 2a skeleton+venv started
- **User reported:** counting clear via speakers (no earphones available — accepted as good enough for Step 1).
- **Step 1 done:** 5-sec mono 16kHz WAV records + plays. Source/sink understood.
- **Next:** Step 2a — `voice-assistant/` skeleton + `.venv` + `sounddevice numpy`; paste install output; then Step 2b `recorder.py`.

### 2026-09-21 — Session 7 (cont. 4): __init__.py question asked
- **User asked:** what is `__init__.py` and what does it do (didn't know at all).
- **Answer given:** marks `assistant/` as a Python package (importable folder); empty file is fine; enables `from assistant.recorder import ...`.
- **Still pending:** paste output of Step 2a install block (last 5 lines or full error).
- **Next:** Step 2b `recorder.py` once venv confirmed.
