# HANDOFF / LOG — voice-assistant workshop

> **Purpose:** continue anywhere (Windows opencode, Linux opencode, new chat) without missing anything.
> **Rule for AI:** after EVERY reply/conversation, append a new entry to `## Log` below (date, what user asked, what you did, decisions, next step). Keep it detailed but factual. Never delete old entries.

---

## 1. Current status (update this block each time)

- **Date:** 2026-09-12
- **Phase:** Planning done, starting Module 0 (Windows practice OK, real build on Linux)
- **Files:** `PLAN.md` ✅, `HANDOFF.md` ✅, `PROGRESS.md` ✅, `WINDOWS_PRACTICE.md` ✅, `AGENTS.md` ✅ (portable mentor instructions)
- **Next step for user:** do `WINDOWS_PRACTICE.md` Part 1 on Windows (30-60 min), then copy `PLAN.md` + `AGENTS.md` + `PROGRESS.md` to Linux CachyOS machine and paste the Role prompt from `AGENTS.md` into Linux opencode.
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
