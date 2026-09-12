# WINDOWS PRACTICE — Module 0 prep (no Linux needed)

> Do this on Windows this week (~1 hr). Goal: get fluent enough that Linux Modules 1-3 don't stall on Python.
> On Linux your mentor will redo the Needle part natively — here we just build muscle.

## Part 1 — venv + pip (15 min)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install cactus-needle
python -c "import needle; print('needle ok')"
```

**In your own words, write:** what is a venv? Why do we always use one?
(Hint: isolated Python folder so project packages don't fight system packages.)

If `Activate.ps1` is blocked: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

## Part 2 — your first Needle tool (25 min)

Save as `toy.py`, run with `python toy.py`:

```python
import needle

@needle.tool
def add(a: int, b: int):
    """Add two numbers together."""
    return {"result": a + b}

@needle.tool
def get_weather(city: str):
    """Get the current weather for a city."""
    return {"city": city, "temp_c": 27, "sky": "clear"}

agent = needle.Needle(tools=[add, get_weather])
print(agent.run("what is 4 + 5?")["results"])
print(agent.run("what's it like in Lagos right now?")["results"])
```

Then answer:
1. What does the docstring (`"""..."""`) do for Needle? (It's the tool description the model reads — good descriptions = correct picks.)
2. Break it on purpose: change the `add` docstring to `"Do stuff."` and rerun. What happens? Change it back.
3. Add a third tool `greet(name: str)` returning `{"hello": name}` and call it via `agent.run("greet Ana")`.

Set `NEEDLE_TELEMETRY=0` if you want no anonymous telemetry: `$env:NEEDLE_TELEMETRY="0"`.

## Part 3 — functions + JSON + errors (20 min)

```python
import json

def set_volume(level: int):
    """Set speaker volume 0-100."""
    if not 0 <= level <= 100:
        raise ValueError("level must be 0-100")
    return {"volume": level}

print(json.dumps(set_volume(30)))   # what does dumps do? (dict -> JSON text)
try:
    set_volume(999)
except ValueError as e:
    print("caught:", e)             # read this: last line of a traceback tells the cause
```

**Challenge:** write `open_app(name: str)` that only allows `"firefox"`, `"kitty"`, `"nautilus"` (raise ValueError otherwise). This previews our v1 allowlist idea.

## Done when…

- [ ] You can create/activate a venv from memory
- [ ] You can explain: venv, pip, function, docstring, JSON, traceback (last line first)
- [ ] `toy.py` runs and you added one tool yourself

Paste any error's **last 5 lines** to your mentor — that's where the cause lives. Log this session in `PROGRESS.md`.
