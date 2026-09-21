# MCMIO — tools

Software for **Misure di Campi Meccanici con Immagini e Onde**. Everything here is free, and most of it is open source, so you can install it on your own machine and keep using it after the exam.

Start with the two or three tools that match your project. You are not expected to know all of this.

---

## Foundations

Used by nearly everything below.

- **[OpenCV](https://opencv.org/)** — the standard computer vision library. Calibration, feature tracking, optical flow. `pip install opencv-python`
- **[scikit-image](https://scikit-image.org/)** — image processing in Python, with excellent documentation and examples. `pip install scikit-image`
- **[Fiji / ImageJ](https://fiji.sc/)** — the general-purpose image workbench. Fast for looking at a stack, measuring something, or trying a filter before you write any code.

## Displacement and strain fields — DIC

- **[Ncorr](http://www.ncorr.com/)** — open-source 2D DIC for MATLAB, with a GUI. The usual starting point.
  Tutorials: [Part 1 — running an analysis](https://www.youtube.com/watch?v=cXfeiBXjN18) · [Part 2 — Ncorr_post post-processing](https://www.youtube.com/watch?v=D4Q_d31iPUk) · [source](https://github.com/justinblaber/ncorr_2D_matlab)
- **[pyidi](https://github.com/ladisk/pyidi)** — image-based displacement identification in Python, from LADISK. Built for vibration: subpixel methods on high-speed sequences. `pip install pyidi`
- **[DICe](https://github.com/dicengine/dice)** — Sandia's DIC engine. C++ with a GUI, handles 2D and stereo, good for larger datasets.
- **[µDIC](https://github.com/PolymerGuy/muDIC)** — fully open Python DIC, useful when you want to see and modify what the algorithm does. `pip install muDIC`
- **[py2DIC](https://github.com/Geod-Geom/py2DIC)** — lightweight Python 2D DIC, easy to read as a reference implementation.

## Motion amplification and optical flow

- **[Phase-based video motion processing](http://people.csail.mit.edu/nwadhwa/phase-video/)** — MIT CSAIL. Makes invisible vibration visible; the papers and code are the reference for phase-based methods.
- Optical flow — Farnebäck and Lucas–Kanade are both in OpenCV, and are the quickest way to get a first displacement field out of a sequence.

## Infrared thermography

- **[pyFlir](https://github.com/LolloCappo/pyFlir)** — reading and controlling FLIR scientific cameras. `pip install pyFlir`
- **[InfraPy](https://github.com/LolloCappo/InfraPy)** — processing, analysis and visualization of infrared data. `pip install InfraPy`
- **[pyLIA](https://github.com/LolloCappo/pyLIA)** — lock-in analysis, for thermoelastic stress analysis. `pip install pyLIA`
- **[pysfmov](https://github.com/LolloCappo/pysfmov)** — SFMOV file reader. `pip install pysfmov`
- **[flirpy](https://github.com/LJMUAstroecology/flirpy)** — alternative reader for consumer and research FLIR formats, useful when a file will not open elsewhere.

## 3D shape and scanning

- **[Meshroom](https://alicevision.org/)** — free photogrammetry with a node-based GUI. Reconstructs 3D geometry from a set of photographs.
- **[COLMAP](https://colmap.github.io/)** — structure-from-motion and multi-view stereo. More control than Meshroom, less hand-holding.
- **[CloudCompare](https://www.cloudcompare.org/)** — point cloud and mesh comparison. This is the tool for "how far is the scan from the CAD model".
- **[MeshLab](https://www.meshlab.net/)** — mesh cleaning, simplification and conversion.

## Flow fields — PIV

- **[OpenPIV](http://www.openpiv.net/)** — open-source particle image velocimetry, in [Python](https://github.com/OpenPIV/openpiv-python) and MATLAB. `pip install openpiv`
- **[PIVlab](https://github.com/Shrediquette/PIVlab)** — MATLAB PIV with a GUI and a large set of video tutorials. The gentler entry point.

## Acoustic fields

- **[Acoular](https://acoular.org/)** — acoustic beamforming in Python: microphone array processing and acoustic maps, i.e. an acoustic camera in software. `pip install acoular`

## Vibration and modal analysis

- **[sdypy](https://github.com/sdypy/sdypy)** — structural dynamics in Python, an umbrella over several tools.
- **[pyEMA](https://github.com/ladisk/pyEMA)** — experimental modal analysis: FRFs, pole identification, mode shapes. `pip install pyEMA`

## Reference data and reading

- **[iDICs DIC Challenge](https://idics.org/challenge/)** — benchmark image sets with known displacement fields. The right way to check whether your DIC pipeline is actually correct, rather than merely producing output.
- **[digitalimagecorrelation.org](https://digitalimagecorrelation.org/)** — practical guidance on speckle patterns, lighting and common DIC mistakes.

---

Something here refuses to install, or you think a tool is missing? Open an [issue](../../../../issues).
