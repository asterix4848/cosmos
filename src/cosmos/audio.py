"""Best-effort system-audio loopback capture via soundcard/PulseAudio."""
from __future__ import annotations

import threading
import time

import numpy as np


class AudioAnalyzer:
    """Captures the default output monitor and exposes smoothed frequency bands."""

    def __init__(self, sample_rate: int = 22050, chunk: int = 2048) -> None:
        self.sample_rate = sample_rate
        self.chunk = chunk
        self._lock = threading.Lock()
        self._levels = np.zeros(3, dtype=np.float32)
        self.status = "Audio loopback is starting…"
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._capture, daemon=True)
        self._thread.start()

    def bands(self) -> tuple[float, float, float]:
        with self._lock:
            return tuple(float(x) for x in self._levels)

    def close(self) -> None:
        self._stop.set()

    def _capture(self) -> None:
        try:
            import soundcard as sc

            speaker = sc.default_speaker()
            if speaker is None:
                self.status = "No default audio output; visualizer is in idle mode"
                return
            mic = sc.get_microphone(id=str(speaker.name), include_loopback=True)
            self.status = f"Listening to system audio: {speaker.name}"
            frequencies = np.fft.rfftfreq(self.chunk, 1 / self.sample_rate)
            while not self._stop.is_set():
                data = mic.record(numframes=self.chunk, samplerate=self.sample_rate)
                if data.size == 0:
                    continue
                mono = np.mean(data, axis=1) if data.ndim > 1 else data
                spectrum = np.abs(np.fft.rfft(mono * np.hanning(len(mono))))
                bands = []
                for low, high in ((30, 180), (180, 2000), (2000, 9000)):
                    part = spectrum[(frequencies >= low) & (frequencies < high)]
                    bands.append(float(np.sqrt(np.mean(part * part))) if part.size else 0.0)
                # Normalize and smooth to avoid jitter; relative scaling suits typical PCM output.
                target = np.clip(np.asarray(bands, dtype=np.float32) * 18.0, 0.0, 1.0)
                with self._lock:
                    self._levels = self._levels * 0.68 + target * 0.32
        except Exception as exc:  # audio APIs differ across Mint/PulseAudio/PipeWire setups
            self.status = f"System audio unavailable ({type(exc).__name__}); idle animation active"
            while not self._stop.wait(0.25):
                pass
