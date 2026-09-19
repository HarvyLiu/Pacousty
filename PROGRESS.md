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

<!-- Example:
### 2026-09-14 — Module 0 — 60 min
- **Did:** venv + pip install cactus-needle, ran Lagos weather example.
- **Worked:** tool ran, results printed.
- **Didn't / errors:** none.
- **Understood:** venv is an isolated Python folder so packages don't clash.
- **Next:** WINDOWS_PRACTICE Part 2 / Module 1 mic check on Linux.
-->
