# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Harvy
import sys
import time
from faster_whisper import WhisperModel

WAV = sys.argv[1] if len(sys.argv) > 1 else "test_py.wav"
# print(len(sys.argv))

t0 = time.time()
# Fixed zero for computers to count from: 1970-01-01 00:00:00 UTC, called the epoch.
# time.time(), seconds since 1970. t0 is saving the initial time.
model = WhisperModel("base.en", device="cuda", compute_type="float16")
# float16 for less memory usage
print(f"Loaded in {time.time() - t0:.1f}s.")

t1 = time.time()
segments, info = model.transcribe(WAV)
# text = ""
# for s in segments:
#     text = " ".join(s.text.strip())
text = " ".join(s.text.strip() for s in segments)
print(f"text: {text!r}")
print(f"Done in {time.time() - t1:.1f}s, lang={info.language} p={info.language_probability:.2f}.")
