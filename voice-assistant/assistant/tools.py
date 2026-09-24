# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Harvy

from typing import Literal

AppName = Literal["kitty", "nautilus", "brave", "discord"]

# Below are functions for Needle2!
# tests for now

def get_weather(city: str) -> dict:
    '''Get the current weather for a city'''
    return {"city": city, "temp": 27, "sky": "clear"}
def open_app(name: AppName) -> dict:
    '''Open an allowed app by the app's name. Only the tools listed in the variable list, AppName.'''
    if name not in AppName:
        raise ValueError(f"Not allowed: {name}")
    return {"app": name}
def set_volume(level: int) -> dict:
    '''Set speaker volume to a certain level. Level must be 0 to 100.'''
    if not 0<=level<=100:
        raise ValueError(f"Oops, level outta range: {level}")
    return {"volume": level}

