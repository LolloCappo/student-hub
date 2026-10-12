# Model-based design and uncertainty analysis of magnetoresistive probes: from field physics to design laws — research path

**MSc thesis** · Ingegneria Meccanica (LM-33) · Oct 2026 – Mar 2027 · Department of Engineering, Università degli Studi di Perugia · expected graduation April 2027

This is the working plan for the thesis. It tells you what to do, in what order, how to do it, what each step produces, and how you know it is finished. Section 4 breaks it down week by week; section 5 lists what you check all the time, whatever week it is. The plan will change as results come in — that is normal. We review it at every milestone.

**How to use it.** Keep it open. Every Monday, read that week in section 4. Every two weeks, before our meeting, tick what is done and write down what is not and why.

---

## 1. The goal

A magnetoresistive (MR) sensor detects a ferromagnetic target by sensing how the target distorts the field of a bias magnet. You will build a simulator that predicts how well a given probe — magnet, sensor, position — will work, check it against measurements, and then use it to design a probe for a case it has never seen.

**Research question.** Can a validated model of field, sensor and noise, with its uncertainty, design a magnetoresistive probe for a new application without trial and error? And what general laws decide where the optimum lies?

**Hypotheses you will test.** Each of them can turn out false. That is what makes them worth testing.

| | Hypothesis | Why it matters | Tested in |
|---|---|---|---|
| H1 | For μr ≳ 100 the target's permeability barely matters: the signal is set by geometry | the design rule would need no material data | step 8 |
| H2 | For a periodic target (a gear) the signal swing decays roughly as exp(−2πg/p) with air gap g and pitch p, on top of the magnet's own decay; for an isolated target it decays as a power law | the backbone of a closed-form rule: maximum air gap grows with pitch | step 17 |
| H3 | The best sensor position is set by the sensor's working range (saturation, stability), not by where the field changes most | the bias field is tens to hundreds of mT; an MR element saturates at a few mT | steps 7, 14, 17 |
| H4 | In dimensionless form (g/p, magnet size/p, magnet aspect ratio, sensor saturation field/Br) the optima collapse onto a few master curves | one chart covers every application | step 17 |

---

## 2. Choices that shape the whole plan

### How the sensor is modelled: from its datasheet

The sensor model — how output voltage depends on the field — comes from the **datasheet**: typical sensitivity, linear range, saturation field, offset, temperature coefficients. Every datasheet value with a min–max range enters the model as an **uncertainty**: a rectangular distribution between min and max, a "Type B" evaluation in the language of the GUM (JCGM 100). Where only a typical value is given, you decide a range, write down why, and test how much the result depends on it.

Two consequences you must keep in mind throughout:

- The datasheet tells you the *typical* unit, not yours. Sensitivity spreads of ±15–25 % are common. So the validation is **relative**: you compare quantities in which the sensitivity cancels — where the optimum is, the shape of the signal, ratios between configurations measured with the same sensor. Absolute amplitudes are checked only against the datasheet band.
- Datasheets rarely describe the response under a strong field along a second axis, which is exactly what the bias magnet produces. Where the datasheet is silent, state the assumption you make and test how much the result depends on it.

**Optional upgrade — a Helmholtz coil.** If one is available (the physics teaching lab may lend one) or there is time to build one, calibrate the sensor unit used for validation in it. This replaces the datasheet model for that unit, cuts the sensitivity uncertainty to a few per cent, and lets the validation and the blind test become absolute. The plan works without it; step 15 says where it fits if it happens.

### How "best" is measured: one set of quantities, in the model and on the bench

Do not use the RMS of the simulated field: the sensor does not see the field directly, the RMS includes the bias offset, and noise is missing. Use this hierarchy, computed by the simulator and measured on the bench:

| Level | Quantity | Notes |
|---|---|---|
| Field | swing of the field component along the sensitive axis | only where the bias keeps the sensor inside its working range (no saturation, no AMR flipping) |
| Sensor | output swing ΔV, through the datasheet transfer curve | carries the datasheet uncertainty |
| Measurement | SNR = ΔV / noise in the application's bandwidth · for switching: timing jitter σ_t = σ_n / \|dV/dt\| at the threshold · **maximum air gap**: the gap where SNR falls to a set threshold | noise is *measured* on the bench (step 11) |

Maximum air gap is the number industry uses to compare speed sensors. It is your headline result.

### Conventions, fixed once in week 1 and never changed

- **Units:** SI everywhere in code — metres, tesla, A/m. Convert datasheet units on input: 1 Oe = 79.58 A/m, which is 0.1 mT in air; 1 G = 0.1 mT. Most unit errors in this field come from Oe and G.
- **Coordinates:** x = direction of target motion, y = air gap direction (from sensor towards target), z = depth. Origin at the centre of the magnet's face on the sensor side. Draw this in the notes and use it in every figure.
- **The sensor's axes:** state for each sensor which of its axes is the sensitive one and how it is aligned with x, y, z on the bench.

---

## 3. The path, step by step

Each step lists what to do, how, what to watch out for, what it produces, and when it is done. Steps inside a phase can overlap.

### Phase A — Foundations (October)

**Step 1 · Set up.**
- A git repository with this layout: `src/` (code), `sims/` (simulation inputs and cached results), `data/raw/` (measurements exactly as recorded — never edited), `data/processed/`, `notebooks/` (exploration only), `notes/`, `thesis/`.
- A Python environment pinned in a file (`environment.yml` or `requirements.txt`): NumPy, SciPy, Matplotlib, Gmsh (Python API), pyvista and meshio, Magpylib, pandas, h5py.
- Elmer installed and callable from the command line.
- A dated lab notebook — paper or electronic — where everything goes: what you did, settings, file names, surprises.

*Watch out:* install Elmer early; on Windows it can take a day to get right. *Done when* a Python script builds a mesh with Gmsh, runs Elmer on it and reads the result back.

**Step 2 · Physics, limited to what the model needs.** Short notes, not a literature review. Cover:
- **Fields and materials:** B, H, M, B = μ0(H + M); demagnetisation and why the field inside a magnet depends on its shape.
- **The magnet:** remanence Br, coercivity Hc, recoil permeability (about 1.05 for NdFeB), temperature coefficient of Br (about −0.12 %/K for NdFeB); the grades (N35 … N52) and their Br tolerance.
- **The target:** μr, saturation (about 1.5–2 T for steels), and why a soft steel's hysteresis can be ignored here.
- **AMR:** resistance R = R0 + ΔR cos²θ, with ΔR/R of 2–3 %; barber-pole biasing; flipping and set/reset; for small transverse fields, sin θ ≈ Hy / (Hk + Hx) — so a field along the easy axis stabilises the element but reduces its sensitivity.
- **GMR and TMR:** spin valves and tunnel junctions at the level of their transfer curve; linear range, saturation; TMR's higher sensitivity and higher 1/f noise.
- **Bridges and gradiometers:** how four elements make a Wheatstone bridge; how two elements at a spacing reject a uniform external field.
- **Noise:** thermal (√(4kTR), about 4 nV/√Hz for 1 kΩ at room temperature) and 1/f.
- **The Hall sensor** as the baseline: linear over hundreds of mT, lower sensitivity.

Reading: Coey, *Magnetism and Magnetic Materials*; Furlani, *Permanent Magnet and Electromechanical Devices* (analytical magnet fields); Tumanski, *Thin Film Magnetoresistive Sensors*; Ripka (ed.), *Magnetic Sensors and Magnetometers*.

*Produces* a **parameter table** (`notes/parameters.csv` or a sheet) with columns: quantity · symbol · value · unit · source · uncertainty · how the uncertainty was obtained. *Done when* the table is complete for one magnet, one target and the chosen sensors. These notes become chapter 2.

**Step 3 · Verification V1 — the magnet alone.**
- Use an **axisymmetric** 2D model for a cylindrical magnet. A *planar* 2D model represents an infinitely long bar, not a cylinder — mixing the two up is the most common mistake here.
- Compare the on-axis field with the analytical formula. For a magnet of radius R and length L, at a distance z from its face: Bz = (Br/2) · [ (z+L)/√(R²+(z+L)²) − z/√(R²+z²) ].
- Compare off-axis with Magpylib.
- **Mesh study:** refine the mesh near the magnet until the field at a few reference points changes by less than your tolerance. **Air-box study:** enlarge the surrounding air until the same holds. Plot both.

*Watch out:* magnetisation is entered in A/m (Br/μ0), and its sign sets the field direction. *Produces* a convergence plot and a short note with the chosen mesh and air-box size. *Done when* Elmer and the reference agree within a tolerance you state and justify — for example 1 % within 2 magnet diameters.

**Step 4 · Verification V2 — a permeable body.** A long permeable cylinder in a uniform transverse field (planar 2D). Inside it the field is uniform and B_in = 2μr / (μr + 1) · B0 — compare it, and the field outside, with the analytical solution. Impose the uniform field through the boundary conditions.
*Done when* agreement is within the stated tolerance for μr from 10 to 1000.

**Step 5 · Choose and order the hardware.** University procurement takes weeks, so do it now. Before buying, check each datasheet for: linear range, sensitivity with min–max, noise density, bridge resistance, supply, and **a drawing of where the sensing element sits in the package**.
- **Sensors:** one AMR and one TMR, plus a Hall sensor — all with **raw analog bridge outputs**. ICs with on-chip processing hide the transfer curve. Buy several units of each, and evaluation boards if they exist.
- **Magnets:** NdFeB cylinders and blocks in three or four sizes, of a known grade.
- **Targets:** steel bars of a few widths, of a known steel grade; a gear or a toothed bar for the periodic case.
- **Motion and positioning:** a linear stage with an encoder (resolution 10 µm or better, travel 50 mm or more); an XYZ micrometer stage for the sensor; feeler gauges for setting the air gap.
- **Electronics:** a stable bridge supply, a low-noise instrumentation amplifier, a DAQ (16-bit at least, 24-bit better) that can sample the encoder and the sensor together.
- **Mechanics:** aluminium profiles and **brass or aluminium screws** — no steel parts within about 5 cm of the sensor.
- **Field reference:** a calibrated 3-axis Hall probe or gaussmeter — borrow if possible, and get its calibration certificate.

*Done when* everything is ordered or located, with a list of expected delivery dates.

**Milestone M1 (end of October):** V1 passes, parameter table complete, hardware ordered.

### Phase B — The simulator (November)

**Step 6 · Datasheet sensor model.**
- One Python function per sensor type: `output_voltage(Hx, Hy, params)`, returning volts for given field components (in A/m) and a parameter set.
- **Linear part:** V = Vs · (S · H_sensitive + offset), with Vs the supply and S the sensitivity in V/V per A/m.
- **Saturation:** smooth, for example a tanh, matched to the datasheet's typical curve.
- **AMR specifics:** the effect of the field along the easy axis on sensitivity (from step 2), and a flag when the field could flip the element.
- **Parameters:** each with its typical value and its min–max range, so the function can be called with random samples.
- **Tests:** small automatic tests that check units and that the typical curve matches the datasheet plot.

*Done when* the model reproduces the datasheet's typical curve and its spread can be sampled.

**Step 7 · Simulator v1 in 2D.**
- **Geometry:** a parametric Gmsh model — magnet, air gap, target — with the target moved along x and the mesh rebuilt at each position. Refine the mesh in a small rectangle where the sensor can sit.
- **Solve and extract:** run Elmer, read the result with pyvista, and interpolate Bx and By on a grid of candidate sensor positions (for example every 0.1 mm).
- **Sensor and performance:** apply the sensor model at each grid point, then compute swing, SNR (with a placeholder noise until step 11) and maximum air gap.
- **Cache everything:** store each result with its input parameters and the git commit hash, so that nothing is solved twice and every figure can be traced to its run.
- **Two rules keep it fast:** one solve gives the field everywhere, so every sensor position is free; and the swing needs only the target positions that give the extremes — full sweeps are needed only to compare waveforms.

*Watch out:* planar 2D assumes everything is infinitely deep. It is a model of a long bar target, not of a gear tooth of finite width; step 15 measures how much that matters. *Done when* one command goes from design parameters to a performance map, and a log tells you how long each solve took.

**Step 8 · H1 — does μr matter?**
- Sweep the target's μr from 10 to 5000 on a log scale, for two or three geometries. Look at the swing and at where the optimum is.
- Check one case with a non-linear B–H curve for the steel: is the target saturated anywhere near the magnet?

*Done when* you can state the μr above which the result changes by less than a stated amount, and whether the target saturates.

**Step 9 · Uncertainty of the prediction.**
- Monte Carlo over the inputs: datasheet ranges, magnet Br tolerance, positioning tolerance (sensor position, air gap).
- **This needs no new solves.** With linear materials the field is proportional to Br, so Br is a scale factor; a position error is an interpolation in the stored field map; the datasheet ranges only enter the sensor model. A few thousand samples take seconds.
- Find which input dominates: vary one at a time, or compute variance-based (Sobol) indices with SALib.

*Done when* the simulator returns every prediction as a value with a band, and you know which input dominates it.

**Milestone M2 (end of November):** the 2D simulator gives performance maps with uncertainty bands; H1 answered.

### Phase C — The bench and the validation (December–January)

**Step 10 · Build the bench.**
- Target on the linear stage, sensor on the XYZ micrometer stage, magnet fixed behind the sensor. A rigid frame; no steel near the sensor.
- Encoder and sensor sampled together, so every reading has a target position.
- **Reference position:** find where the target's edge is in encoder coordinates — for example where the signal crosses a set level on the way in and on the way out.
- **Air gap:** set it with feeler gauges or the micrometer, and write down its uncertainty.
- **Procedure for every sweep:** warm up for 30 minutes; move slowly (a few mm/s — the model is magnetostatic); always approach from the same direction (backlash); log the room temperature; repeat each sweep at least three times.

*Produces* a written measurement procedure (`notes/procedure.md`) that anyone could follow. *Done when* a sweep produces output vs target position, and repeats agree within a stated repeatability.

**Step 11 · Noise, measured in place.**
- Target at rest, everything powered. Record long enough — at least ten times the period of the lowest frequency you care about.
- Compute the power spectral density (Welch's method). Look for mains pickup at 50 Hz and its harmonics, and remove its cause.
- Integrate the spectrum over the application's bandwidth (set by the tooth frequency range) to get the noise in volts. Report the noise density at 1 Hz and at 1 kHz, and compare with the datasheet.
- Measure with and without the bias magnet: the bias changes the sensor's operating point, and with it the noise.

*Done when* the simulator uses the measured noise instead of the placeholder.

**Step 12 · Validation A — the field.**
- With the calibrated Hall probe on the XYZ stage, map the bare magnet's field on a grid, then the field with the target at a few positions.
- Uncertainty on the measured side: the probe's calibration, the size and position of its active area, positioning.
- Compare with the simulator using the approach of ASME V&V 20: comparison error E = S − D (simulation minus data) and validation uncertainty u_val = √(u_num² + u_input² + u_D²), with u_num from the convergence study, u_input from step 9 and u_D from the measurement.

This validates the field model independently of any MR sensor. *Done when* agreement is quantified as E against u_val, not just plotted.

**Step 13 · Where the die really is.** The sensing element sits somewhere inside the package, uncertain by about ±0.1–0.2 mm — comparable to the width of the optimum. Scan the sensor across a sharp feature (the magnet's edge, or a thin steel pin), compare where the signal's feature falls with where the model puts it, and fit the offset in x and y. Do it for every unit you use.
*Done when* the die position of each unit is known with a stated uncertainty.

**Mid-term review (mid-December, before the break):** what works, what does not, and the scope for January–March — whether to run 3D, how many sensor types, whether the coil (step 15) is worth it.

**Step 14 · Validation B — the sensor output, relative.**
- **Measurement grid:** for example 5 sensor positions × 4 air gaps × 2 magnets, each sweep repeated three times, all with the same sensor unit.
- Compare with the prediction:
  - the **location of the optimum** — fit a parabola around the maximum, in both data and model;
  - the **shape** of the signal, normalised to its own swing;
  - **ratios** — swing at one air gap over swing at another, one magnet over another — in which the sensitivity cancels;
  - the **absolute** swing and SNR, checked against the datasheet band.
- For each quantity: E, u_val, and whether |E| < u_val.

*Done when* each quantity has a comparison error and an uncertainty, and you can say where the model holds and where it does not. If it does not hold, step 12 tells you whether the field or the sensor model is at fault.

**Step 15 · Range of validity.**
- **3D:** run Elmer in 3D on three to five selected cases (finite target width, the real magnet shape) and measure what 2D gets wrong.
- **Speed:** repeat a sweep at increasing speed and find where the waveform changes by more than the repeatability. Eddy currents in the steel are the likely cause; the skin depth δ = √(2/(ωμσ)) is a few tenths of a millimetre in steel at 1 kHz.
- **Optional — the Helmholtz coil:** if available, find its constant (mT per ampere) with the gaussmeter, calibrate the validation sensor unit in it, map its response to two field components by rotating it inside the coil, replace its datasheet model, and repeat the absolute comparison of step 14.

*Done when* the range of validity — geometry, speed, μr — is stated.

**Milestone M4 (end of January):** validated simulator, with its uncertainty and its range of validity stated.

### Phase D — Laws and design (February)

**Step 16 · Optimisation.**
- **Surrogate:** choose the design variables (magnet diameter and length, sensor x and y, air gap) and their ranges; run 100–300 designs spread by Latin hypercube sampling; train a fast model (a Gaussian process, scikit-learn) and check it on runs it was not trained on.
- **Robust objective:** for each design, the SNR's mean minus k standard deviations under the tolerances of step 9 — so a design that a 0.1 mm error destroys scores badly.
- **Pareto front:** SNR against magnet volume, with pymoo (NSGA-II).

*Done when* the Pareto front exists for one application, and the surrogate's error is stated.

**Step 17 · The laws.**
- List every variable and its units; form the dimensionless groups (Buckingham π): g/p, magnet diameter/p, magnet length/diameter, sensor position/g, μr, μ0·H_sat/Br.
- Sweep each group in the simulator, for an isolated target and for a periodic one.
- Test H2 (exponential vs power-law decay — plot the swing on log axes against g/p), H3 (where the optimum sits relative to the sensor's working range) and H4 (do curves from different absolute sizes fall on top of each other?).
- Fit what holds into a closed-form rule, and draw it as a design chart.

*Done when* the rule predicts the simulator's optimum within a stated error over a stated range.

**Step 18 · The blind test.**
- With the supervisors, choose an application not used for any tuning — for example, a gear with a given pitch and air gap.
- **Freeze the simulator** (a git tag) and **write the predictions before building**, committed with a date:
  - where the optimum sensor position is;
  - how much larger the swing is than a reference design measured with the same sensor (a ratio, so the sensitivity cancels);
  - the maximum air gap, with its band.
- Build it, measure it with the procedure of step 10, and compare.

Report the result whatever it shows — a failed prediction with a clear reason is a result too. *Done when* predictions and measurements are side by side, with uncertainties.

**Milestone M5 (end of February):** design rule and chart; blind test measured.

### Phase E — Writing and release (March)

**Step 19 · Finish.**
- **Thesis:** complete draft to supervisors in early March; one full revision; submit by the department's deadline for the April session (usually a few weeks before — check it in October, not in March).
- **Code:** a README with installation and an example that reproduces one figure; a licence; tagged release.
- **Data:** the measured data with a description of every file; a DOI on Zenodo.
- **Paper:** a draft built on the design rule and the blind test.
- **Defence:** slides, using the presentation template in the student hub.

---

## 4. Week by week

Weeks run Monday to Friday. Each month ends with what must exist and the questions you must be able to answer at its milestone meeting.

> **Week 1 has already passed.** If anything in it is not done — repository, environment, Elmer, conventions, the thesis deadline — it comes first in week 2, before the reading.

### October 2026 — foundations, tools, orders

| Week | Do | Check before moving on |
|---|---|---|
| **1** · 5–9 Oct | Step 1: repository, environment, Elmer installed. Write the conventions (units, coordinates). Start the notebook. Find the department's thesis deadline for the April session | the Gmsh → Elmer → Python loop runs once |
| **2** · 12–16 Oct | Step 2: notes on fields, magnets, targets. Start the parameter table. Step 5: shortlist sensors (AMR, TMR, Hall) from datasheets — check the element's position drawing | shortlist discussed with supervisors |
| **3** · 19–23 Oct | Step 2: notes on AMR, GMR, TMR, bridges, noise. Step 3: V1 axisymmetric magnet model; mesh and air-box studies. **Place all orders** | orders placed; V1 runs |
| **4** · 26–30 Oct | Step 3 finished. Step 4 started: V2 model. Parameter table completed. Chapter 2 skeleton (headings and key equations) | **M1** |

**End of October — must exist:** convergence plots for V1 · parameter table · order list with delivery dates · conventions note · chapter 2 skeleton.
**Questions for M1:** Which mesh size and air box did you choose, and why? What does the datasheet *not* tell you about each sensor? When does each piece of hardware arrive?
**Decision:** if Elmer still does not run reliably, switch the 2D work to FEMM and keep Elmer for 3D later.

### November 2026 — sensor model and simulator v1

| Week | Do | Check before moving on |
|---|---|---|
| **5** · 2–6 Nov | Step 4 finished (V2 for μr 10–1000). Step 6: sensor models with tests | V2 within tolerance |
| **6** · 9–13 Nov | Step 7: parametric planar geometry, target stepping, field extraction on the sensor grid, caching | one geometry runs end to end |
| **7** · 16–20 Nov | Step 7: sensor model applied; swing, SNR (placeholder noise) and maximum air gap maps. First look at H3: where is the optimum relative to the saturation limit? | maps look physically sensible; the optimum is not at a grid edge |
| **8** · 23–27 Nov | Step 8 (μr sweep, saturation check). Step 9 (Monte Carlo, dominant input). Chapter 2 finished; chapter 3 skeleton. As hardware arrives: check every part against its order and log serial numbers | **M2** |

**End of November — must exist:** sensor-model code with tests · simulator v1 with caching and logging · performance maps with bands · μr result · chapter 2 draft.
**Questions for M2:** Above which μr does the result stop depending on it? Which input dominates the uncertainty band, and could we reduce it? Is the predicted optimum inside the sensor's working range, and how far from where the field changes most?

### December 2026 — bench and field validation (short month)

| Week | Do | Check before moving on |
|---|---|---|
| **9** · 30 Nov–4 Dec | Step 10: frame, stages, magnet and sensor mounts, wiring; encoder and DAQ sampled together | a first sweep is recorded with positions |
| **10** · 7–11 Dec | Step 10: reference position, air-gap setting, written procedure, repeatability. Step 11: noise spectrum and bandwidth noise | three repeats agree; no 50 Hz pickup left |
| **11** · 14–18 Dec | Step 12: Hall-probe field maps, E against u_val. Step 13: die position of each unit. **Mid-term review** | field validated or the discrepancy understood |
| 21 Dec – 6 Jan | Holidays. If you want to work: write chapter 3 (the simulator). No lab work alone | — |

**End of December — must exist:** working bench and its procedure · noise spectra and bandwidth noise · field-level validation table · die positions · mid-term review notes with the agreed scope.
**Questions for M3:** How repeatable is the bench, in µm and in mV? Does the field model agree with the Hall probe within u_val — and if not, where and why? What did we decide about 3D, sensor types and the coil?

### January 2027 — sensor-level validation

| Week | Do | Check before moving on |
|---|---|---|
| **12** · 7–8 Jan | Re-check the bench after the break: one reference sweep compared with December's | the reference sweep matches |
| **13** · 11–15 Jan | Step 14: the measurement grid with the first magnet | all sweeps recorded and logged |
| **14** · 18–22 Jan | Step 14: the second magnet; comparison of optimum location, shapes, ratios, absolute band | E and u_val for every quantity |
| **15** · 25–29 Jan | Step 15: 3D cases; speed sweep; the coil if it was agreed. Chapter 3 finished; chapter 4 started | **M4** |

**End of January — must exist:** validation table (quantity · E · u_val · pass/fail) · 3D vs 2D comparison · speed limit · chapter 3 draft.
**Questions for M4:** Where does the model hold, and where does it not? Is a failure in the field or in the sensor model? How fast can the target move before the static model breaks?
**Decision:** if the relative validation fails and step 12 passed, the sensor model is at fault — that is when the coil stops being optional.

### February 2027 — laws, design, blind test

| Week | Do | Check before moving on |
|---|---|---|
| **16** · 1–5 Feb | Step 16: design variables and ranges, Latin hypercube runs, surrogate trained and checked. **Agree the blind-test application with the supervisors** | surrogate error stated; application fixed |
| **17** · 8–12 Feb | Step 16: robust objective, Pareto front. Step 17: dimensionless groups, sweeps for isolated and periodic targets | sweeps complete |
| **18** · 15–19 Feb | Step 17: test H2, H3, H4; fit the rule; draw the design chart. Step 18: **freeze the simulator, commit the predictions**, build the blind-test probe | predictions committed before any measurement |
| **19** · 22–26 Feb | Step 18: measure and compare. Chapter 4 finished; chapter 5 drafted | **M5** |

**End of February — must exist:** Pareto front · design rule and chart with its range and error · committed predictions and the blind-test measurements · chapter 4 draft, chapter 5 draft.
**Questions for M5:** Which hypotheses held? What is the design rule, and over which range is it valid? Did the blind test land inside its band — and if not, why?

### March 2027 — writing and release

| Week | Do | Check before moving on |
|---|---|---|
| **20** · 1–5 Mar | Introduction and conclusions written. **Complete draft to supervisors** | the whole thesis exists, rough or not |
| **21** · 8–12 Mar | Revise from supervisors' comments. Code: README, example, licence, tag. Data on Zenodo | another person can reproduce one figure |
| **22** · 15–19 Mar | Final revision; figures and references checked. Paper draft | thesis ready to submit |
| **23–25** · 22 Mar–9 Apr | Submit by the department's deadline. Defence slides; two rehearsals | thesis submitted; slides rehearsed |

**End of March — must exist:** submitted thesis · public code and data · paper draft · defence slides.

---

## 5. Things you check all the time

Whatever week it is, these apply.

**Every week**
- Lab notebook up to date, with dates.
- Code committed and pushed; raw data backed up in two places.
- Parameter table and uncertainty notes updated with anything new.
- At least one finished figure or paragraph added to the thesis folder.

**Before every meeting (every two weeks)**
- A one-page note: what you did, what you found, what is blocking you, what you will do next.
- This plan ticked: what is done, what slipped, why.

**Every simulation**
- The run's parameters and the git commit are stored with its result.
- When the geometry changes significantly, re-check mesh convergence on one case.
- Units checked at the boundary between datasheet and code.

**Every measurement session**
- Warm-up, room temperature logged, sensor and magnet serial numbers written down.
- A **reference sweep** at the start — the same configuration every day — compared with the first one ever recorded. If it moved, find out why before measuring anything else.
- Every sweep repeated at least three times; raw files never edited; file names `YYYYMMDD_runNN_short-description`.

**Every result**
- A value with its uncertainty, and a sentence on where the uncertainty comes from.
- Compared with something: the model, the previous measurement, a hand estimate. A number compared with nothing is not a result yet.

---

## 6. The thesis, chapter by chapter

| Chapter | Content | Built from | Drafted in |
|---|---|---|---|
| 1 Introduction | the problem, the research question, the hypotheses, what is new | section 1 of this plan | March |
| 2 Physics and sensors | fields, magnets, targets, MR and Hall sensors, noise | step 2 | Oct–Nov |
| 3 The simulator | geometry, solver, verification V1–V2, sensor models, performance measures, uncertainty | steps 3–4, 6–9 | Nov–Jan |
| 4 Bench and validation | bench, procedure, noise, field validation, die position, sensor-level validation, range of validity | steps 10–15 | Jan–Feb |
| 5 Laws and design | optimisation, dimensionless laws, design rule and chart, blind test | steps 16–18 | Feb |
| 6 Conclusions | answers to the research question and to H1–H4, limits, future work | everything | March |
| Appendices | parameter table, procedure, code and data description | | as you go |

---

## 7. Scope and risks

**Needed to graduate:** verified 2D simulator · datasheet sensor model for one MR sensor type, with uncertainty · noise measured in place · field-level and relative sensor-level validation · design rule for isolated and periodic targets · one blind test.

**If time allows:** Helmholtz-coil calibration and absolute validation · 3D beyond the validity check · the second MR type and a technology map (AMR vs TMR vs Hall) · the full Pareto analysis · a submitted paper.

**Decision points**

| When | Question | If no |
|---|---|---|
| end of October | does Elmer run reliably from Python? | FEMM for 2D; Elmer only for 3D |
| mid-December | is the bench repeatable, and the field validated? | fix the bench before any sensor-level work; cut the second sensor type |
| end of January | does the relative validation pass? | if the field passed, the sensor model is at fault: build or borrow the coil |
| mid-February | is the blind-test application fixed and the simulator frozen? | no measurement until both are done |

**Known risks**

| Risk | What we do |
|---|---|
| Elmer with permanent magnets takes long to learn | start V1 in week 3 at the latest; fall back on FEMM (2D) or Magpylib if it stalls |
| hardware arrives late | order in October; build the simulator while waiting |
| the datasheet spread hides model errors | relative validation; the coil (step 15) if it becomes necessary |
| positioning uncertainty dominates | micrometer stage, written procedure, die-position calibration (step 13) |
| steel parts near the sensor distort the field | aluminium and brass only within 5 cm; check with the Hall probe |
| the scope grows | the mid-term review decides what is cut |

---

## 8. How we work

- We meet every two weeks. Before each meeting, send the one-page note of section 5.
- Everything goes in git — code, data, figures, notes. No `final_v3.py`.
- The lab notebook is dated and complete: settings, sensor serial numbers, positions, file names.
- Write as you go. A chapter drafted in the month it happens takes a week; written in March, it takes a month.
- Tell us when you are stuck. Stuck is normal; stuck and silent for three weeks is the only real problem.
