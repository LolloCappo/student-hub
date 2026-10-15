"""Synthetic speckle images with a known displacement, for testing pyIDI.

Every speckle is a Gaussian spot integrated exactly over the area of each pixel,
so moving the pattern by a fraction of a pixel is rendered exactly: there is no
interpolation, and the displacement you impose is the ground truth.

Usage
-----
    python synthetic_speckle.py --out runs/baseline        # the baseline case of the plan
    python synthetic_speckle.py --motion ramp --amplitude 2 --out runs/ramp_A2
    python synthetic_speckle.py --help

Each run writes a folder with the frames and settings.json, which holds everything
needed to compute the true displacement again with true_displacement(). Up to 8 bits
the frames are PNG images: open the first one with pyidi.VideoReader. Above 8 bits,
or with --npy, they are one array, frames.npy:

    video = VideoReader(np.load("folder/frames.npy"), root="folder")
"""
import argparse
import json
from pathlib import Path

import imageio.v3 as iio
import numpy as np
from scipy.special import erf

MOTIONS = ("static", "ramp", "sine", "two-sine", "rotation", "beam")


def speckle_centres(shape, d, fill, seed):
    """Random speckle centres (row, col), spots of diameter d px covering about `fill` of the area."""
    rng = np.random.default_rng(seed)
    margin = 3 * d + 20                       # speckles outside the frame keep the edges speckled when it moves
    h, w = shape[0] + 2 * margin, shape[1] + 2 * margin
    n = int(fill * h * w / (np.pi * d ** 2 / 4))
    return rng.uniform(-margin, shape[0] + margin, n), rng.uniform(-margin, shape[1] + margin, n)


def render(cy, cx, d, shape):
    """Image of the speckles centred at (cy, cx): each spot's light integrated over every pixel."""
    s = np.sqrt(2) * d / 4                    # sigma = d / 4
    ey = np.arange(shape[0] + 1) - 0.5        # pixel edges; pixel (i, j) is centred on (i, j)
    ex = np.arange(shape[1] + 1) - 0.5
    gy = np.diff(erf((ey[None, :] - cy[:, None]) / s), axis=1) / 2
    gx = np.diff(erf((ex[None, :] - cx[:, None]) / s), axis=1) / 2
    ink = gy.T @ gx                           # each whole spot carries 1
    peak = 1 / (2 * np.pi * (d / 4) ** 2)     # centre value of an isolated spot
    return 1 - np.exp(-ink / peak)            # 0 = background, close to 1 where spots overlap


def true_displacement(rows, cols, t, p):
    """True (row, col) displacement in px of the material points at (rows, cols), at times t in s.

    rows and cols are the positions in the first frame, t = frame index / fps; the result has
    shape (len(rows), len(t), 2), in the same order as pyIDI's displacements.
    """
    rows, cols, t = np.atleast_1d(rows).astype(float), np.atleast_1d(cols).astype(float), np.atleast_1d(t)
    t = np.clip(t - p["still"] / p["fps"], 0, None)   # the target is still for the first `still` frames
    a, f = p["amplitude"], p["frequency"]
    dy = np.zeros((rows.size, t.size))
    dx = np.zeros((rows.size, t.size))
    ux, uy = np.cos(np.radians(p["angle"])), -np.sin(np.radians(p["angle"]))   # direction: 0 deg = +col, 90 deg = up
    if p["motion"] == "ramp":                 # from 0 to `amplitude` in equal steps, one per frame
        s = a * t / t[-1] if t[-1] > 0 else 0 * t
        dx[:], dy[:] = ux * s, uy * s
    elif p["motion"] == "sine":
        s = a * np.sin(2 * np.pi * f * t)
        dx[:], dy[:] = ux * s, uy * s
    elif p["motion"] == "two-sine":           # a second component, at 2.7 f and a third of the amplitude
        s = a * np.sin(2 * np.pi * f * t) + a / 3 * np.sin(2 * np.pi * 2.7 * f * t + 1.0)
        dx[:], dy[:] = ux * s, uy * s
    elif p["motion"] == "rotation":           # rigid rotation about the image centre; amplitude in degrees
        th = np.radians(a) * np.sin(2 * np.pi * f * t)
        y0, x0 = (p["height"] - 1) / 2, (p["width"] - 1) / 2
        ry, rx = rows[:, None] - y0, cols[:, None] - x0
        dy = rx * np.sin(th) + ry * np.cos(th) - ry
        dx = rx * np.cos(th) - ry * np.sin(th) - rx
    elif p["motion"] == "beam":               # first bending mode of a cantilever clamped at col 0; amplitude at the tip
        def mode(z):
            return np.cosh(z) - np.cos(z) - 0.7341 * (np.sinh(z) - np.sin(z))
        phi = mode(1.8751 * cols / (p["width"] - 1)) / mode(1.8751)   # 1 at the free end
        dy = -a * phi[:, None] * np.sin(2 * np.pi * f * t)[None, :]
    return np.stack([dy, dx], axis=-1)


def make_video(p):
    """Frames as floats in 0..1 (before noise and quantisation) and the frame times."""
    shape = (p["height"], p["width"])
    cy, cx = speckle_centres(shape, p["d"], p["fill"], p["seed"])
    t = np.arange(p["frames"]) / p["fps"]
    u = true_displacement(cy, cx, t, p)
    frames = np.empty((p["frames"], *shape))
    for k in range(p["frames"]):
        frames[k] = render(cy + u[:, k, 0], cx + u[:, k, 1], p["d"], shape)
    return frames, t


def digitise(frames, p):
    """Grey levels as a camera would store them: contrast, flicker, noise, then rounding to `bits` bits."""
    rng = np.random.default_rng(p["seed"] + 1)
    lo, hi = 0.5 - p["contrast"] / 2, 0.5 + p["contrast"] / 2
    gain = 1 + p["flicker"] * rng.standard_normal(len(frames))[:, None, None]   # the light changes from frame to frame
    img = gain * (lo + (hi - lo) * frames) + rng.normal(0, p["noise"], frames.shape)
    top = 2 ** p["bits"] - 1
    return np.clip(np.round(img * top), 0, top).astype(np.uint8 if p["bits"] <= 8 else np.uint16)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--motion", choices=MOTIONS, default="sine")
    ap.add_argument("--amplitude", type=float, default=0.3, help="px (degrees for rotation; tip displacement for beam)")
    ap.add_argument("--angle", type=float, default=0.0, help="direction of a translation, degrees: 0 = +col, 90 = up")
    ap.add_argument("--frequency", type=float, default=5.0, help="Hz")
    ap.add_argument("--fps", type=float, default=200.0, help="frames per second")
    ap.add_argument("--frames", type=int, default=200)
    ap.add_argument("--still", type=int, default=20, help="frames at the start with no motion: the reference")
    ap.add_argument("--height", type=int, default=128)
    ap.add_argument("--width", type=int, default=256)
    ap.add_argument("--d", type=float, default=4.0, help="speckle diameter, px")
    ap.add_argument("--fill", type=float, default=0.5, help="fraction of the area covered by speckles")
    ap.add_argument("--contrast", type=float, default=0.8, help="grey-level range used, fraction of full scale")
    ap.add_argument("--noise", type=float, default=0.005, help="standard deviation, fraction of full scale")
    ap.add_argument("--flicker", type=float, default=0.0, help="standard deviation of the brightness from frame to frame, fraction")
    ap.add_argument("--bits", type=int, default=8, help="bit depth; above 8 the PNGs are 16-bit")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--npy", action="store_true", help="write frames.npy instead of PNGs, at any bit depth")
    ap.add_argument("--out", default="synthetic")
    p = vars(ap.parse_args())

    out = Path(p["out"])
    if out.exists() and any(out.iterdir()):   # old frames or analyses would no longer match settings.json
        raise SystemExit(f"{out} is not empty: choose a new --out folder")
    out.mkdir(parents=True, exist_ok=True)
    frames, t = make_video(p)
    images = digitise(frames, p)
    if p["bits"] <= 8 and not p["npy"]:
        for k, im in enumerate(images):
            iio.imwrite(out / f"frame_{k:05d}.png", im)
        name = "frame_00000.png ..."
    else:                                     # 16-bit PNGs are read back big-endian, which Lucas-Kanade rejects;
                                              # an array also loads much faster than PNGs, for scripted sweeps
        np.save(out / "frames.npy", images)
        name = "frames.npy"
    (out / "settings.json").write_text(json.dumps(p, indent=2))
    print(f"{len(images)} frames of {p['height']} x {p['width']} px written to {out}/{name}")


if __name__ == "__main__":
    main()
