"""Cosmos real-time 3D Big Bang visualizer."""
from __future__ import annotations

import math
import random
import time

import numpy as np
from panda3d.core import (
    AmbientLight, AntialiasAttrib, DirectionalLight, Geom, GeomNode,
    GeomPoints, GeomVertexData, GeomVertexFormat, GeomVertexWriter,
    NodePath, TransparencyAttrib, Vec3, Vec4, WindowProperties,
)
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task

from .audio import AudioAnalyzer


class Cosmos(ShowBase):
    def __init__(self, fullscreen: bool = False) -> None:
        super().__init__()
        self.disableMouse()
        self.setBackgroundColor(0.008, 0.012, 0.035, 1)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        props = WindowProperties()
        props.setTitle("Cosmos — Music Reactive Universe")
        props.setCursorHidden(False)
        if fullscreen:
            props.setFullscreen(True)
        self.win.requestProperties(props)
        self.camera.setPos(0, -38, 8)
        self.camera.lookAt(0, 0, 0)
        self.setFov(68)

        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.42, 0.46, 0.68, 1))
        self.render.setLight(self.render.attachNewNode(ambient))
        key = DirectionalLight("key")
        key.setColor(Vec4(0.65, 0.76, 1.0, 1))
        key_np = self.render.attachNewNode(key)
        key_np.setHpr(-25, -55, 0)
        self.render.setLight(key_np)

        self._make_core()
        self._make_stars()
        self._make_particles()
        self.audio = AudioAnalyzer()
        self.started = time.monotonic()
        self.paused = False
        self.audio_text = OnscreenText(text="Starting audio…", pos=(-1.29, 0.93), scale=0.038,
                                       fg=(0.68, 0.78, 1, 0.9), align=0, mayChange=True)
        OnscreenText(text="COSMOS", pos=(-1.29, 0.84), scale=0.055,
                     fg=(0.88, 0.92, 1, 0.95), align=0)
        OnscreenText(text="SPACE pause   F fullscreen   ESC quit", pos=(1.28, -0.94), scale=0.033,
                     fg=(0.62, 0.68, 0.82, 0.8), align=2)
        self.accept("escape", self.userExit)
        self.accept("space", self.toggle_pause)
        self.accept("f", self.toggle_fullscreen)
        self.taskMgr.add(self.update_scene, "cosmos-update")

    def _make_core(self) -> None:
        # Luminous origin: layered translucent spheres read as a compact primordial singularity.
        for radius, color in ((1.15, (0.28, 0.54, 1.0, 0.11)),
                              (0.64, (0.42, 0.72, 1.0, 0.18)),
                              (0.22, (0.9, 0.97, 1.0, 0.85))):
            core = self.loader.loadModel("models/misc/sphere")
            core.reparentTo(self.render)
            core.setScale(radius)
            core.setColor(*color)
            core.setTransparency(TransparencyAttrib.MAlpha)
            core.setDepthWrite(False)
            self.cores = getattr(self, "cores", []) + [core]

    def _make_stars(self) -> None:
        fmt = GeomVertexFormat.getV3c4()
        data = GeomVertexData("background-stars", fmt, Geom.UHStatic)
        data.setNumRows(900)
        vw, cw = GeomVertexWriter(data, "vertex"), GeomVertexWriter(data, "color")
        rng = random.Random(41)
        for _ in range(900):
            direction = np.array([rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)])
            direction /= np.linalg.norm(direction)
            radius = rng.uniform(27, 55)
            vw.addData3f(*(direction * radius))
            brightness = rng.uniform(0.35, 0.95)
            cw.addData4f(brightness, brightness * 0.9, 1.0, rng.uniform(0.4, 0.9))
        prim = GeomPoints(Geom.UHStatic)
        prim.addNextVertices(900)
        geom = Geom(data)
        geom.addPrimitive(prim)
        node = GeomNode("starfield")
        node.addGeom(geom)
        self.render.attachNewNode(node).setRenderModeThickness(2.0)

    def _make_particles(self) -> None:
        self.count = 2600
        rng = np.random.default_rng(17)
        dirs = rng.normal(size=(self.count, 3)).astype(np.float32)
        dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
        # A modest equatorial bias creates filament and galaxy-like structure.
        dirs[:, 2] *= 0.62
        dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
        self.directions = dirs
        self.radii = rng.uniform(1.1, 22, self.count).astype(np.float32)
        self.speeds = rng.uniform(0.45, 1.4, self.count).astype(np.float32)
        self.phases = rng.uniform(0, math.tau, self.count).astype(np.float32)
        self.hues = rng.uniform(0, 1, self.count).astype(np.float32)
        self.fmt = GeomVertexFormat.getV3c4()
        self.data = GeomVertexData("expanding-universe", self.fmt, Geom.UHDynamic)
        self.data.setNumRows(self.count)
        self.vertex_writer = GeomVertexWriter(self.data, "vertex")
        self.color_writer = GeomVertexWriter(self.data, "color")
        prim = GeomPoints(Geom.UHStatic)
        prim.addNextVertices(self.count)
        geom = Geom(self.data)
        geom.addPrimitive(prim)
        node = GeomNode("cosmic-particles")
        node.addGeom(geom)
        self.cloud = self.render.attachNewNode(node)
        self.cloud.setRenderModeThickness(3.0)
        self.cloud.setTransparency(TransparencyAttrib.MAlpha)
        self.cloud.setDepthWrite(False)

    def update_scene(self, task: Task) -> int:
        dt = min(globalClock.getDt(), 0.05)
        low, mid, high = self.audio.bands()
        if not self.paused:
            elapsed = time.monotonic() - self.started
            self.radii += self.speeds * dt * (0.22 + low * 1.8)
            wrapped = self.radii > 25
            self.radii[wrapped] = 0.8
            wobble = np.sin(elapsed * 0.8 + self.phases) * (0.035 + mid * 0.16)
            positions = self.directions * (self.radii + wobble[:, None])
            self.vertex_writer = GeomVertexWriter(self.data, "vertex")
            self.color_writer = GeomVertexWriter(self.data, "color")
            for i, (x, y, z) in enumerate(positions):
                self.vertex_writer.setData3f(float(x), float(y), float(z))
                # Blue, violet and warm golden filaments.
                hue = self.hues[i]
                pulse = min(1.0, 0.34 + self.radii[i] / 36 + high * 0.45)
                if hue < 0.58:
                    col = (0.24 * pulse, 0.48 * pulse, 1.0 * pulse)
                elif hue < 0.86:
                    col = (0.78 * pulse, 0.32 * pulse, 1.0 * pulse)
                else:
                    col = (1.0 * pulse, 0.68 * pulse, 0.34 * pulse)
                self.color_writer.setData4f(*col, 0.42 + 0.5 * pulse)
            self.cloud.setScale(1.0 + low * 0.055)
            for n, core in enumerate(self.cores):
                base = (1.0, 0.56, 0.2)[n]
                core.setScale(base * (1 + low * (0.35 if n == 2 else 0.16)))
            self.camera.setX(math.sin(elapsed * 0.09) * 1.3)
            self.camera.setZ(8 + math.sin(elapsed * 0.13) * 0.7)
            self.camera.lookAt(0, 0, 0)
        self.audio_text.setText(self.audio.status)
        return Task.cont

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def toggle_fullscreen(self) -> None:
        props = WindowProperties()
        props.setFullscreen(not self.win.getProperties().getFullscreen())
        self.win.requestProperties(props)

    def destroy(self) -> None:
        self.audio.close()
        super().destroy()


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="A cinematic music-reactive 3D universe")
    parser.add_argument("--fullscreen", action="store_true", help="start in fullscreen")
    args = parser.parse_args()
    Cosmos(fullscreen=args.fullscreen).run()


if __name__ == "__main__":
    main()
