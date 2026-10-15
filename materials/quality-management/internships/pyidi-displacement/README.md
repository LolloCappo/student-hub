# How well does a camera measure displacement?

**Internship project** · Quality Management · BSc Engineering Management (L-8) · two students, one shared project · about 12 weeks, rescaled to the hours of your internship agreement

*Image-based displacement identification with [pyIDI](https://github.com/ladisk/pyidi): Simplified Optical Flow and Lucas–Kanade, from synthetic images to real measurements.*

---

## In one paragraph

A camera can measure how a part moves at thousands of points at once, without touching it. Whether that measurement can be trusted depends on choices the user makes: the method, the region analysed, the size of the subsets, the pattern on the target, and how far the target moves. In this internship you find out how much each of those choices matters. You work with pyIDI, an open-source Python package for image-based displacement identification, and you start from **synthetic images of a target moved by a known amount** — so the true displacement is known exactly, and every error can be measured instead of guessed. Each of you takes one method: one studies **Simplified Optical Flow (SOF)**, the other **Lucas–Kanade (LK)**. Each maps where the method works, where it fails, and which settings give the best result. Together you turn the two maps into a short guide for choosing a method and its settings, and test that guide on a few real measurements.

## Why this is a quality problem

- Cameras measure displacement and vibration in end-of-line testing, modal testing and structural monitoring: one camera can replace many contact sensors.
- Before any instrument is used to make decisions, quality management asks three questions: **how large is its error, does the error depend on what is measured, and how repeatable is it?** In a measurement system analysis (MSA) these are the *bias*, the *linearity* and the *repeatability* of the instrument.
- For a camera there is no datasheet value to look up: the answer depends on the method, on its settings and on the target. This project produces that answer for two methods, together with a procedure for choosing the settings.
- It uses the course directly: sampling, quantisation and aliasing (lecture 8), sensor noise (lecture 9), lighting (lecture 10), and the statistics of lecture 6.

## Two tracks, one project

| | Track A | Track B |
|---|---|---|
| **Method** | Simplified Optical Flow (SOF) | Lucas–Kanade (LK) |
| **Its natural range** | displacements well below one pixel | from hundredths of a pixel to several pixels |
| **The central question** | how small a motion it sees, and where its linear range ends | how large a motion it follows, and what the subset size costs |
| **What you will learn to control** | point placement, averaging, the reference image | subset size, interpolation, convergence |

**What is shared:** the synthetic videos (the same files for both of you), the metrics and the script that computes them, the run log, the real measurements, and the final comparison. The two tracks only make sense together if their numbers can be compared, so the shared rules come first (phase A).

## The words we use

- **Displacement identification** — computing from a sequence of images how far each point of a target has moved, relative to a reference image. The result is in pixels; the pixel size on the object (lecture 8) converts it to millimetres.
- **Region of interest (ROI)** — the area of the image you analyse, drawn in the GUI as a rectangle or a polygon.
- **Grid and cells** — inside the ROI the GUI lays a regular grid of cells, with one measuring point at the centre of each. A cell is as large as the subset; *noverlap* is the number of pixels that neighbouring cells share, so the spacing between points is the subset size minus noverlap.
- **Subset** — the small window of pixels around a point that the method works on. In SOF, the image is averaged over the subset before the gradient is computed; in LK, the subset is the template that is tracked from frame to frame.
- **Speckle pattern** — a random pattern of spots painted or printed on the target, so that every subset has texture to follow. The **speckle size** is the diameter of a spot, in pixels.
- **Reference image** — the image the motion is measured from: one frame, or the average of several frames in which the target is still.
- **Error** — the identified displacement minus the true displacement, at each point and in each frame.

## The two methods

### Track A — Simplified Optical Flow (SOF)

- **What it is** — each point's displacement comes from one division: the change in brightness relative to the reference image, divided by the brightness gradient at that point (Javh et al., 2017).
- **Why it matters** — there is no iteration, so it is extremely fast: thousands of points over long recordings, and very sensitive to small motions.
- **How it works, and its limits**
  - it assumes that brightness changes linearly with position, which holds only for motions well below one pixel;
  - it sees only the component of the motion along the local gradient: a point on a vertical edge sees horizontal motion, and nothing else;
  - any change in brightness that is not caused by motion — noise, flickering light — is read as motion.
- **Its settings in pyIDI** — subset size, the points (a grid in the ROI, or points chosen where the gradient is strong in the direction of motion), the reference range (the frames averaged into the reference), `mean_n_neighbours`, `pixel_shift` (from a script only), `convert_from_px`.

### Track B — Lucas–Kanade (LK)

- **What it is** — template tracking: the subset around a point in the reference image is shifted, with sub-pixel interpolation, until it matches the current frame as closely as possible. The shift that gives the best match is the displacement (Lucas & Kanade, 1981).
- **Why it matters** — it follows displacements from hundredths of a pixel to several pixels, in both directions at once. It is pyIDI's default method.
- **How it works, and its limits**
  - it iterates, so it is slower than SOF;
  - the subset needs texture in both directions;
  - it assumes the subset only translates: rotation or strain inside the subset becomes an error;
  - the interpolation used for sub-pixel shifts can add a small systematic error that depends on the fractional part of the displacement — well known in digital image correlation, and something you will look for.
- **Its settings in pyIDI** — subset size (vertical × horizontal), the points (grid in the ROI and noverlap), `pad`, `max_nfev` (maximum iterations), tolerance, `int_order` (interpolation order), the reference image.

## The synthetic images

The generator is [`synthetic_speckle.py`](synthetic_speckle.py), in this folder. It draws a speckle pattern in which each spot is integrated exactly over the area of every pixel, so a shift of a fraction of a pixel is rendered exactly, with no interpolation. **The displacement you impose is the ground truth.** Each run writes the frames into a new folder, together with `settings.json`, which holds every setting of the run. The function `true_displacement()` turns those settings into the true displacement at any point and any frame.

```
python synthetic_speckle.py --motion sine --amplitude 0.3 --out runs/sine_A0.3
python synthetic_speckle.py --help
```

Every video starts with 20 still frames (`--still`), which can serve as the reference. The motions grow in difficulty; work through them in order.

| Level | Motion | Example options | What it tests |
|---|---|---|---|
| 0 | none | `--motion static --noise 0.01` | the noise floor: what the method reports when nothing moves |
| 1 | ramp, from 0 to the amplitude in equal steps | `--motion ramp --amplitude 2` | bias and linearity over the whole range; systematic sub-pixel errors |
| 2 | sine in one direction | `--motion sine --amplitude 0.3 --angle 45` | the amplitude and phase of a vibration; the effect of its direction |
| 3 | two sines | `--motion two-sine` | whether a small second component survives |
| 4 | rigid rotation | `--motion rotation --amplitude 0.5` | a displacement field that varies across the image |
| 5 | first bending mode of a cantilever | `--motion beam --amplitude 0.5` | a mode shape, as in modal testing |
| 6 | any of the above, degraded | `--noise`, `--flicker`, `--contrast`, `--bits` | the camera and the lighting (lectures 9 and 10) |

You will extend the generator when the plan needs something it does not do yet — blur, uneven light, a pattern printed at a given dpi. Keep the rule: **every video is fully described by its `settings.json`, and the truth is computed from it.**

## What you measure

Every quantity is computed by the same shared script, in pixels, for each direction separately (rows and columns).

| Quantity | Definition | In MSA terms |
|---|---|---|
| **Bias** | mean error over all points and frames | bias |
| **Random error** | standard deviation of the error | repeatability |
| **Noise floor** | standard deviation of the identified displacement on a still video | resolution |
| **Linearity** | slope of identified against true displacement on a ramp, and the largest deviation from that line | linearity |
| **Amplitude error** | identified amplitude ÷ true amplitude − 1, for the sines, at the known frequency | — |
| **Crosstalk** | displacement reported in the direction that does not move | — |
| **Failed points** | share of points that return no value, or an error larger than 0.5 px | — |
| **Run time** | seconds per 1000 point-frames, on the same computer | — |

**Every number comes with its spread.** Repeat each case with at least three speckle patterns (`--seed 0`, `1`, `2`) and report the mean and the standard deviation across them: that is a Type A evaluation of uncertainty. Use the same seeds in both tracks, so both methods see the same patterns.

## What you vary

**Baseline** — every study starts from it and changes one thing: speckle size 4 px, `--fill 0.5`, `--contrast 0.8`, `--noise 0.005`, 8 bits, a sine of 0.3 px at 0°, 200 frames with 20 of them still. These are the generator's defaults, so `python synthetic_speckle.py --out runs/baseline` makes it. Subset 3 for SOF and 15 × 15 for LK.

**Shared factors — the target and the camera**

| Factor | Option | Suggested values |
|---|---|---|
| Speckle size | `--d` | 1, 2, 3, 4, 6, 8, 12 px |
| Displacement magnitude | `--amplitude` | 0.01, 0.03, 0.1, 0.3, 0.5, 1, 2, 5 px |
| Direction of motion | `--angle` | 0°, 30°, 45°, 90° |
| Speckle density | `--fill` | 0.3, 0.5, 0.7 |
| Image noise | `--noise` | 0, 0.005, 0.01, 0.02 of full scale |
| Contrast | `--contrast` | 0.2, 0.5, 0.8 |
| Bit depth | `--bits` | 6, 8, 12 |
| Flicker | `--flicker` | 0, 0.005, 0.02 |

**Track A — SOF settings**

| Setting | Where | Suggested values |
|---|---|---|
| Subset size | GUI, *Set points* | 1, 3, 5, 7, 11 |
| Points | GUI grid, or `SelectionGUI` with the *Gradient in direction* evaluator | both, compared |
| Grid spacing | GUI, *noverlap* | from cells that just touch to one point every pixel |
| Reference range | GUI, *Configure* | 1, 5 and 20 still frames |
| `mean_n_neighbours` | GUI, *Configure* | 0, 4, 16 |
| `pixel_shift` | script only | off, on |

**Track B — LK settings**

| Setting | Where | Suggested values |
|---|---|---|
| Subset size (h × w) | GUI, *Set points* | 5, 9, 15, 21, 31; also non-square |
| Grid spacing | GUI, *noverlap* | as for SOF |
| `max_nfev` | GUI, *Configure* | 5, 10, 20, 50 |
| Tolerance | GUI, *Configure* | 1e-3, 1e-5, 1e-8 |
| `int_order` | GUI, *Configure* | 3 (the fast compiled path) against 1 |
| Reference image | script | frame 0, or the average of the still frames |

**How to vary them.** First one factor at a time around the baseline, to see each effect on its own. Then, for the three or four factors that matter most, a small factorial design — every combination of two levels of each, 8 or 16 runs — to see whether factors interact: does the best subset size depend on the speckle size?

## Questions each track answers

Each starts as a hypothesis, and each can turn out false — that is what makes it worth testing.

| | Hypothesis | Why it matters | Phase |
|---|---|---|---|
| **A1** | SOF underestimates the amplitude as the motion grows; there is a magnitude above which the error exceeds 5 %, and it depends on the speckle size and the subset size | the linear range: the first number a user of SOF needs | B |
| **A2** | Larger subsets or larger speckles extend the linear range but raise the noise floor | the central trade-off of SOF | B |
| **A3** | Points chosen where the gradient lies along the motion are far more accurate than a regular grid | how to place SOF points | B |
| **A4** | Flicker and image noise appear as false motion, larger where the gradient is weak | why lighting matters (lecture 10) | C |
| **B1** | LK's random error falls as the subset grows, roughly in proportion to 1 / subset width | the cost of a small subset | B |
| **B2** | In a field that varies (rotation, beam), a large subset averages the motion away: there is an optimum subset size | spatial detail against noise | C |
| **B3** | Speckles smaller than about 2–3 px produce a systematic error that repeats with every pixel of motion — aliasing (lecture 8) | the design rule for the target | B |
| **B4** | LK's error does not depend on the magnitude up to a limit, beyond which it loses track; the limit depends on subset and speckle size | the usable range of LK | B |
| **J1** | For motions below about 0.1 px, SOF is as accurate as LK, in a fraction of the time | when to choose SOF | E |
| **J2** | One speckle size, in pixels, serves both methods well | the target for the real measurements | D |

## The path, phase by phase

The weeks assume about twelve weeks; at the first meeting we rescale them to the hours of your internship agreement.

### Phase 0 — Start (week 1)
- Install pyIDI with its GUI (`pip install "pyidi[qt]" scipy`), and set up a shared git repository: one folder per track, plus a shared `common/` with the generator and the evaluation script.
- Read the pyIDI documentation pages on basic usage, the methods, point selection and the napari GUI. Read the paper behind your method.
- Generate the baseline video, open it in the GUI, compute displacements with your method, and compare them with the truth (see *Getting started* below).

*Done when* each of you has computed the error of one run with your own method and shown it in a plot.

### Phase A — Shared foundations (weeks 2–3, together)
- Write the shared evaluation script: it reads a video's `settings.json` and a pyIDI analysis folder, and returns every quantity in *What you measure*. Both of you use it, unchanged, for every run.
- Agree the run log: one row per analysis — the video's settings, the method's settings, the metrics.
- Run levels 0 and 1 at the baseline with both methods: noise floor and linearity.
- Check the truth itself: LK with a large subset on a clean ramp should give an error close to zero. If it does not, the problem is in the comparison, not in the method — find it before going on.

*Milestone M1 (end of week 3):* both tracks report noise floor and linearity at the baseline, computed by the same script.

### Phase B — One factor at a time (weeks 4–6, each on your own track)
- For each new case, look at it first in the GUI: draw the ROI, change a setting, see how the displacement vectors change. Then run the full sweep from a short script that uses the same settings.
- Sweep your method's settings and the shared factors on levels 1 and 2. Answer A1–A3 or B1, B3 and B4.
- One figure per sweep: the error against the factor, with its spread across seeds, and one sentence that says what it shows.

*Milestone M2 (end of week 6):* you present your results to each other and to us. We choose the factors for the factorial design and fix the equipment for phase D.

### Phase C — Harder motions and interactions (weeks 7–8)
- Levels 3 to 6: two sines, rotation, beam, degraded images. Answer A4 or B2.
- The small factorial design on the factors chosen at M2.
- Write your track's **settings guide**: one page that starts from what the user knows (expected motion, speckle size, noise) and ends with the settings to use, and the error to expect.

*Done when* the guide predicts the error of a case it was not built from — generate one together, and check.

### Phase D — Real measurements (weeks 9–10, together)
- **Design the target from your results:** choose the speckle size in pixels (J2), convert it to millimetres with the pixel size on the object, and print the pattern at that size.
- **Record** with the lab's camera: still frames (noise floor); known static steps on a micrometer stage (bias and linearity); a vibration on a shaker, measured at the same time by a reference sensor (amplitude). The equipment is fixed at M2.
- Analyse the same recordings with both methods, and compare the errors with what your synthetic results predicted.

*Done when* every real result sits next to its synthetic prediction, with uncertainties, and every difference has an explanation or an open question.

### Phase E — Comparison and report (weeks 11–12, together)
- The comparison: SOF against LK, case by case — accuracy, range, run time. Answer J1.
- The **joint guide**: which method, and which settings, for which measurement.
- One report, written with the [lab-report template](../../../thesis/lab-report): shared chapters on the problem, the synthetic images and the real measurements, and one chapter per track. A 15-minute presentation, given together.
- Code, run log and the settings of every video in the repository; the videos themselves can always be regenerated.

## Getting started

**Generate a video and open it in the GUI**

```
python synthetic_speckle.py --motion sine --amplitude 0.3 --out runs/sine_A0.3
```

```python
from pyidi import VideoReader, GUI

video = VideoReader("runs/sine_A0.3/frame_00000.png")
gui = GUI(video)
```

In the napari window:
1. **Method selection** — choose Simplified Optical Flow or Lucas–Kanade, then *Confirm method*.
2. **Area Selection** layer — draw the ROI as a rectangle or a polygon. Use the *Area Deselection* layer to cut out parts of it.
3. **Set points** — set the subset size and noverlap, then *Set points*. *show_subset_box* draws the cells.
4. **Configure** — the method's settings, then *Configure*.
5. **Calculate displacements** — the displacements are drawn as vectors on the image. They are in `gui.method.displacements`, and the points in `gui.method.points`.

**Every analysis is saved automatically**, also from the GUI, in a folder next to the video: `frame_00000_pyidi_analysis/analysis_001/`, then `analysis_002/`, and so on. Each folder holds the points (`points.pkl`), the displacements (`results.pkl`) and the method's settings (`settings.json`). Write the analysis number in your lab notebook next to what you were testing.

**Compare an analysis with the truth**

```python
import json
import pickle

import numpy as np

from synthetic_speckle import true_displacement

video_dir = "runs/sine_A0.3"
analysis = f"{video_dir}/frame_00000_pyidi_analysis/analysis_001"

p = json.load(open(f"{video_dir}/settings.json"))
points = pickle.load(open(f"{analysis}/points.pkl", "rb"))     # (n_points, 2): row, col
d = pickle.load(open(f"{analysis}/results.pkl", "rb"))         # (n_points, n_frames, 2): row, col, px

t = np.arange(d.shape[1]) / p["fps"]
truth = true_displacement(points[:, 0], points[:, 1], t, p)
err = d - truth
print("bias (row, col), px:        ", np.nanmean(err, axis=(0, 1)))
print("random error (row, col), px:", np.nanstd(err, axis=(0, 1)))
```

**From a script, for the sweeps**

```python
import numpy as np
from pyidi import VideoReader, SimplifiedOpticalFlow, LucasKanade

video = VideoReader(np.load("runs/sweep_d4/frames.npy"), root="runs/sweep_d4")   # written with --npy
points = np.load("points.npy")              # saved from the GUI with np.save("points.npy", gui.method.points)

lk = LucasKanade(video)
lk.set_points(points)
lk.configure(roi_size=(15, 15))
d = lk.get_displacements()

sof = SimplifiedOpticalFlow(video)
sof.set_points(points)
sof.configure(subset_size=3, reference_range=(0, 20))   # the 20 still frames
d = sof.get_displacements()
```

Write sweep videos with `--npy`: one array loads many times faster than a folder of PNGs.

**Things that will catch you out**
- **SOF's default reference is the average of frames 0 to 100.** If the target moves within them, the reference is wrong. Set the reference range to the still frames, 0 to 20.
- SOF warns *Displacement larger than 0.5 pixel*: the motion has left its linear range.
- SOF on a regular grid: a point where the gradient is zero returns no value (`nan`), and a point where it is weak returns a very noisy one. Count them as failed points — and see A3 for the cure.
- With `mean_n_neighbours` above 0, SOF returns fewer rows than there are points. Average the truth in the same way before you compare.
- Coordinates are (row, column), and rows grow downwards: a motion upwards is a negative row displacement.
- Above 8 bits the generator writes `frames.npy` instead of PNGs: 16-bit PNGs are read back in a byte order that the fast LK code rejects.
- Never reuse a video folder: old analyses would no longer match the new `settings.json`. The generator refuses to write into a folder that is not empty.

## How we work

- We meet every two weeks, and whenever you are stuck. Before each meeting, send a short note: what you did, what you found, what is blocking you.
- Everything goes in git — code, run log, figures, notes. No `final_v3.py`.
- A dated lab notebook: what you ran, with which settings, the analysis number, and what surprised you.
- A number compared with nothing is not a result yet: compare it with the truth, with the other method, or with the previous run.
- Tell us when you are stuck. Being stuck is normal; being stuck in silence for two weeks is the only real problem.

## Useful background

Helpful, but you can pick most of it up along the way:

- Basic Python — NumPy arrays and Matplotlib plots
- The course's lectures on digital images (8), camera sensors (9) and light (10)
- No prior image processing needed

## Reading

- pyIDI documentation: [pyidi.readthedocs.io](https://pyidi.readthedocs.io/en/latest/) — *Basic usage*, *Displacement identification methods*, *Point selection*, *Napari image viewer*
- Javh, J., Slavič, J., Boltežar, M. (2017). The subpixel resolution of optical-flow-based modal analysis. *Mechanical Systems and Signal Processing*, 88, 89–99. [doi:10.1016/j.ymssp.2016.11.009](https://doi.org/10.1016/j.ymssp.2016.11.009) — Track A
- Lucas, B. D., Kanade, T. (1981). An iterative image registration technique with an application to stereo vision. *Proceedings of the 7th IJCAI*, 674–679 — Track B
- Baker, S., Matthews, I. (2004). Lucas–Kanade 20 years on: a unifying framework. *International Journal of Computer Vision*, 56(3), 221–255. [doi:10.1023/B:VISI.0000011205.11775.fd](https://doi.org/10.1023/B:VISI.0000011205.11775.fd) — Track B, sections 1–3
- Pan, B., Qian, K., Xie, H., Asundi, A. (2009). Two-dimensional digital image correlation for in-plane displacement and strain measurement: a review. *Measurement Science and Technology*, 20(6), 062001. [doi:10.1088/0957-0233/20/6/062001](https://doi.org/10.1088/0957-0233/20/6/062001) — both tracks: speckle patterns, subset size, sub-pixel errors
- AIAG, *Measurement Systems Analysis* reference manual — bias, linearity and repeatability, for the quality side
