# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Harvy
import wave
import numpy as np 
import sounddevice as sd 

RATE = 16000
SECS = 5
OUT = "test_py.wav"

print("Recording 5s...")
audio = sd.rec(int(RATE*SECS), samplerate=RATE, channels=1, dtype='int16')
sd.wait()
peak = float(np.abs(audio).max())
# 
print(f"peak level: {peak:.0f} / 32767")
#
with wave.open(OUT, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(audio.tobytes())
print(f"saved {OUT}, {SECS}s mono {RATE}Hz")

