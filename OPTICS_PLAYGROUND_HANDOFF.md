# Optics Playground — Project Handoff for a New Chat

## 1. Project purpose

This project is an interactive single-page HTML teaching site called **Optics Playground**.

It is intended primarily for **Year 1 / Foundations of Physics students** and should teach geometrical and introductory wave optics through interactive diagrams rather than through long blocks of text.

The site owner/author is:

**Joe Chen**  
Centre for Photonics, Department of Physics, University of Bath.

The live GitHub Pages site is:

`https://joe851642001.github.io/optics_playground/`

The GitHub repository is:

`optics_playground`

GitHub Pages is deployed from:

- branch: `main`
- folder: `/(root)`

---

# 2. Core design philosophy

The site should feel like a **physics playground**, not a conventional lecture-note webpage.

Important preferences:

- concise
- visually clean
- physics-correct
- appropriate for first-year university students
- interactive rather than text-heavy
- minimal scrolling
- diagrams should occupy unused white space where possible
- use the same visual language across activities
- avoid unnecessary controls
- controls should manipulate quantities that teach an important physical idea
- avoid adding features simply because they are technically possible
- numerical values and labels should update live
- the physical meaning of an interaction should be obvious from the diagram

Where possible, each activity should use:

1. a large interactive diagram on the left
2. compact controls on the right
3. a 2×2 set of live-value/result cards below the diagram
4. a short **What to look for** explanation

The page should remain usable on smaller screens using a responsive one-column layout.

---

# 3. Visual style

## Typography

Use **Source Sans 3** throughout the site.

Google Fonts import:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">
```

CSS stack:

```css
"Source Sans 3","Segoe UI",Arial,sans-serif
```

Canvas text should use the same stack.

The site currently redraws canvases after:

```js
document.fonts.ready
```

Do not introduce Courier, Aptos, or other unrelated fonts.

---

# 4. Critical Google Analytics requirement

**Every future edit must check that Google Analytics is still embedded.**

Measurement ID:

```text
G-VB4PLZGGJV
```

The following GA4 snippet must remain in `<head>`:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VB4PLZGGJV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VB4PLZGGJV');
</script>
```

Tracking helper:

```js
function track(eventName, params = {}) {
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, params);
  }
}
```

Existing custom events include:

- `tab_opened`
- `simulation_started`
- `ray_limit_explored`
- `tir_reached`
- `critical_angle_reached`
- `preset_used`

Current `simulation_started` activities include:

- `wave_to_ray`
- `refraction`
- `lens`
- `mirror`
- `microscope`
- `telescope`
- `aberrations`

No Plausible analytics references should exist.

After every edit:

1. verify GA loader
2. verify `gtag('config', 'G-VB4PLZGGJV')`
3. verify tracking helper
4. check that no `plausible` reference exists

This is a standing project requirement.

---

# 5. Current tab structure

The current intended tab order is:

1. **Waves → Rays**
2. **Refraction**
3. **Lens**
4. **Mirror**
5. **Microscope**
6. **Telescope**
7. **Aberrations**

The following tabs were deliberately removed:

- Interference
- Diffraction
- Polarisation
- Quantum Optics

Do not restore them unless explicitly requested.

---

# 6. General compactness

The user strongly prefers compact simulation frames and minimal vertical scrolling.

Current approximate canvas/frame sizes:

- Lens canvas: `860 × 400`
- Mirror canvas: `860 × 400`
- Microscope canvas: `860 × 390`
- Telescope canvas: `860 × 390`
- Aberrations canvas: `860 × 390`
- Wave canvas: `330 × 440`
- Refraction SVG visual height: about `360px`

Where empty horizontal space exists, use it before increasing page height.

---

# 7. Waves → Rays tab

Purpose:

Connect diffraction to the geometrical-ray limit.

Model:

Single-slit diffraction at fixed wavelength

```text
λ = 650 nm
```

Controls:

- slit width `a`
- screen distance `L`

Initial slit width:

```text
100 μm
```

Internally fixed spatial screen resolution:

```text
Δx = 0.20 mm
```

Physics:

\[
I(x)\propto \operatorname{sinc}^2\left(\frac{\pi a x}{\lambda L}\right)
\]

First minimum:

\[
x_1 \approx \frac{L\lambda}{a}
\]

Central maximum width:

\[
2L\lambda/a
\]

Buttons:

- **Strong diffraction**
- **Toward ray limit**

User prefers small schematic arrowheads.

Current wave metrics were moved into unused left-column space rather than a full-width strip.

---

# 8. Refraction tab

Purpose:

Interactive Snell's law and total internal reflection.

Controls:

- `n1`
- `n2`
- incident angle

Physics:

\[
n_1\sin\theta_1=n_2\sin\theta_2
\]

The activity includes:

- live ray geometry
- TIR challenge
- critical angle
- presets
- mini challenge

Ray colours:

- incident ray: blue
- refracted ray: red

The Snell's-law result is placed inline under the three main statistics.

The **What is happening?** and **Mini challenge** cards are side-by-side on wide screens.

Avoid duplicate element IDs, especially `substitution`.

---

# 9. Lens tab

Tab name should remain:

**Lens**

not “Lenses”.

Uses a thin-lens approximation and Lensmaker relation.

Physics:

\[
\frac{1}{f}=(n-1)\left(\frac{1}{R_1}-\frac{1}{R_2}\right)
\]

and

\[
\frac{1}{f}=\frac{1}{s_1}+\frac{1}{s_2}
\]

Controls include:

- first surface: convex / concave / plano
- second surface: convex / concave / plano
- radii
- refractive index
- object distance
- presets

The lens is drawn visually thin.

Object and image are represented by tree drawings.

Three principal rays are shown.

Important visual convention:

- one principal ray is now **purple** rather than red
- green central ray passes exactly through the calculated image-tree tip
- focal points are purple dots

Focal-point style precedent:

```js
ctx.fillStyle = '#7b61ff';
ctx.beginPath();
ctx.arc(x, axisY, 5, 0, Math.PI * 2);
ctx.fill();
```

Labels are:

- `F`
- `F′`

This visual convention is reused elsewhere.

---

# 10. Mirror tab

Tab name should remain:

**Mirror**

not “Curved Mirror”.

Uses the spherical/paraxial mirror approximation.

Controls:

- concave / convex
- `|R|`
- object distance
- presets

Physics:

\[
f=\frac{R}{2}
\]

\[
\frac{1}{f}=\frac{1}{s_1}+\frac{1}{s_2}
\]

\[
m=-\frac{s_2}{s_1}
\]

Object and image use tree drawings.

Three principal rays are shown.

One principal ray was changed from red to **purple** to match the Lens tab.

For convex mirrors:

- green construction line toward virtual focus is dotted
- green dashed back-extension of reflected horizontal ray passes through the virtual image-tree tip

---

# 11. Microscope tab

Tab label:

**Microscope**

Panel heading:

**Microscope with a human eye**

This is a compound microscope model with:

- fixed objective
- fixed eyepiece
- fixed human-eye lens
- fixed retina
- adjustable object distance

Current fixed optical parameters:

```text
Objective magnification: 10×
Objective focal length: 20 mm

Eyepiece magnification: 5×
Eyepiece focal length: 50 mm

Human eye lens focal length: 17 mm
```

Important plane positions in the current simulation model:

```text
objective plane = 58.6 mm
eyepiece plane = 240 mm
eye lens plane = 320 mm
retina plane = 337 mm
```

Thus:

```text
retina - eye lens = 17 mm
```

so the retina is at the eye lens back focal plane.

The correct object distance is approximately:

```text
23.6 mm
```

The activity uses a slider for object distance.

Button:

**Set correct focus**

Do not add a “Default View” button unless requested.

Current metric cards:

- Objective 10×
- Eyepiece 5×
- Intermediate-image minus eyepiece-focal-plane offset
- Retina focus error

Visual conventions:

- objective and eyepiece optical planes: purple dotted/dashed
- eye-lens plane: grey
- focal points: purple dots
- first representative ray: purple
- second representative ray: green
- retina: straight vertical red line
- retinal image: small tree
- retinal image becomes blurred if rays do not converge sharply

The intermediate image lies at the **front focal plane of the eyepiece** for relaxed viewing.

Important physics point:

A normal compound microscope with a relaxed eye is **not generally required to be a strict 4f system**.

Required conditions are:

\[
\text{intermediate image}=F_{\rm eyepiece}
\]

and

\[
F'_{\rm eye}\approx \text{retina}
\]

The eyepiece–eye-lens separation is not fixed by the relaxed-eye focusing condition.

Do **not** force:

\[
F'_{\rm eyepiece}=F_{\rm eye}
\]

unless explicitly presenting the special 4f geometry.

---

# 12. Telescope tab

The Telescope tab is implemented as a **Keplerian astronomical telescope with a human eye**.

It deliberately uses similar notation and style to the Microscope tab.

Current parameters:

```text
objective focal length = 120 mm
eyepiece focal length = 24 mm
human eye focal length = 17 mm
```

Normal adjustment:

\[
L=f_{\rm obj}+f_{\rm eye}
\]

so:

```text
L = 144 mm
```

Angular magnification:

\[
M=-\frac{f_{\rm obj}}{f_{\rm eye}}
\]

giving:

```text
M = -5×
```

The negative sign represents an inverted view.

The model shows:

- parallel incoming rays from a distant object
- objective
- real intermediate image
- eyepiece
- human eye lens
- retina

At normal adjustment:

\[
F'_{\rm obj}=F_{\rm eye}
\]

where the objective's rear focal plane is also the eyepiece's front focal plane.

Controls:

- objective–eyepiece separation `L`

Button:

**Set normal adjustment**

The user liked the Microscope-like visual language:

- dotted optical planes
- purple focal dots
- purple + green representative rays
- straight retina
- retinal image tree
- 2×2 live metrics

Moving the eyepiece out of normal adjustment makes the outgoing rays converge/diverge and the fixed eye no longer focuses them exactly on the retina.

---

# 13. Aberrations tab

The Aberrations tab is now a major part of the site.

Current modes:

1. **Spherical**
2. **Chromatic**
3. **Coma**
4. **Astigmatism**
5. **Distortion**

There is also a global comparison:

- **Real lens**
- **Ideal thin lens**

The intention is to make the failure of ideal paraxial optics visually obvious.

---

## 13.1 Spherical aberration

Main control:

- aperture diameter `D`

Parallel rays at different heights are shown.

In the real-lens teaching model:

- marginal rays focus closer to the lens
- paraxial rays focus farther away

Live quantities include:

- aperture
- paraxial focus
- marginal focus
- longitudinal spherical aberration `Δf`

There is a spot inset at the paraxial plane.

Important teaching message:

Closing the aperture removes marginal rays, so the paraxial approximation improves.

---

## 13.2 Chromatic aberration

Modes:

- **White light**
- **Single λ**

Single-wavelength slider:

```text
450–650 nm
```

The teaching model uses a simple wavelength-dependent refractive index.

Shorter wavelengths have larger refractive index and shorter focal length.

Thus:

```text
blue focus closest to lens
green intermediate
red furthest from lens
```

### White-light spot inset

The current design intentionally shows the spot cross-section at the **red focal plane**.

At that plane:

- red = sharpest/smallest spot
- green = larger
- blue = largest

This was deliberately made **visually dramatic**.

Important:

The ray paths and focal-length values remain the physical teaching model, but the **inset blur radii are visually magnified for clarity**.

The webpage explicitly says this.

This magnification is intentional and should not be silently removed.

The main diagram marks the red focal plane.

---

## 13.3 Coma

Coma uses an off-axis point source.

Main control:

- field angle `θ`

The ray diagram shows an off-axis bundle.

The spot inset shows an asymmetric comet-like blur.

Live values include:

- field angle
- paraxial image height
- spot width
- spot asymmetry

Teaching message:

Coma is an off-axis aberration and becomes stronger at larger field angles.

---

## 13.4 Astigmatism

Astigmatism is now designed to be **dynamic**.

Controls:

- field angle `θ`
- **Screen position T → S**

The simulation shows:

- tangential focus `T`
- sagittal focus `S`
- movable observation screen

The observation screen moves continuously between the two focal planes.

The inset morphs continuously:

```text
vertical line
→ ellipse
→ circle of least confusion
→ ellipse
→ horizontal line
```

The inset has a live T-to-S position marker.

The user particularly liked this dynamic implementation.

Teaching message:

For an off-axis point, the tangential and sagittal sections focus at different axial positions.

The circle between them is the **circle of least confusion**.

Do not revert this to the older static three-panel inset unless requested.

---

## 13.5 Distortion

Distortion was added as the fifth aberration mode.

Important conceptual distinction:

**Distortion changes mapping/image position but does not necessarily blur an individual point.**

Controls:

- field angle `θ`
- distortion strength

Distortion strength spans approximately:

```text
-45% to +45%
```

Interpretation:

- negative = barrel
- zero = ideal
- positive = pincushion

The activity shows:

- ideal image position
- actual distorted image position
- a small bundle that still converges to a sharp point

Live values:

- field angle
- ideal image height
- actual image height
- distortion percentage

The dynamic grid inset uses a simple radial teaching model:

\[
r'=r(1+k r^2)
\]

The grid bends continuously:

```text
barrel → ideal → pincushion
```

This is deliberately different from the blur in spherical/coma/astigmatism.

---

# 14. Colours / visual conventions

The project increasingly uses a consistent ray language.

Typical colours:

- blue lens elements: around `#315efb`
- purple main ray / focal points: around `#8b5cf6` or `#7b61ff`
- green secondary ray: around `#117a55`
- red retina / chromatic red ray: around `#dc2626` / `#ef4444`
- blue chromatic ray: `#2563eb`
- green chromatic ray: `#16a34a`
- orange/gold highlights for some marginal/focus indicators: around `#f59e0b` or `#b54708`

Avoid introducing unnecessary new colours.

Purple focal dots are a strong visual convention and should remain consistent.

---

# 15. Footer

Footer text should use:

```text
Joe Chen. Centre for Photonics, Department of Physics, University of Bath. Created by ChatGPT GPT-5.6 Sol on 26/09/2026.
```

Do not change Joe Chen to “Dr Joe Chen” unless explicitly requested.

Analytics privacy wording currently says:

```text
This site uses Google Analytics to understand usage of the teaching activities, including page visits, approximate country and selected interactions. No student name, email address or student ID is requested by this site.
```

Do not claim that the site is fully legally compliant with UK privacy/cookie law without a proper review.

---

# 16. Technical workflow for future edits

The project is currently a single-page HTML application.

Prefer making targeted edits to the latest `index.html`, not rebuilding the entire site from scratch.

After every modification:

1. verify the requested visual/physics changes
2. verify GA4 embed
3. verify no Plausible reference
4. extract the main inline JavaScript
5. run:

```bash
node --check
```

6. create a GitHub-ready ZIP

The final response should normally provide:

- updated `index.html`
- updated `.zip`

---

# 17. Important implementation preferences

When modifying an existing tab:

- preserve current IDs where possible
- avoid duplicate IDs
- do not silently rename tabs
- do not remove current features unless requested
- preserve responsive layout
- preserve Source Sans 3
- preserve analytics
- preserve live redraw after fonts load
- preserve compact frame heights
- do not add long theoretical explanations unless they directly support the interaction

When adding a new optical concept:

1. first identify the one key physical idea
2. design the interaction around that idea
3. keep the number of controls small
4. show the corresponding ray behaviour
5. show a visual image/spot consequence when useful
6. use 2×2 live metric cards
7. add a short “What to look for” section

---

# 18. User design preferences inferred from the project

The user tends to prefer:

- physics diagrams that communicate immediately
- dynamic interactions over static explanatory diagrams
- seeing actual ray behaviour and image consequences
- controls with obvious pedagogical purpose
- consistent notation between related tabs
- focal-point markers
- visually strong effects where subtle physical effects would otherwise be hard to see
- explicit disclosure when a visual effect is exaggerated for clarity
- minimal page clutter
- using available white space rather than increasing vertical height
- matching style across tabs
- visual alignment and precision
- avoiding duplicate status bars or redundant explanatory boxes
- ray intersections landing exactly on image tips when that is the intended physics

If a diagram looks physically or visually ambiguous, improve the diagram rather than adding lots of prose.

---

# 19. Physics accuracy expectations

Physics correctness is important.

If uncertain about a physical claim:

- derive/check it
- use standard optics references if necessary
- distinguish an exact optical result from a simplified teaching model

The site may use simplified pedagogical models, but the webpage should not imply that an intentionally exaggerated or phenomenological model is an exact ray trace.

Examples:

- chromatic spot radii are currently visually magnified for clarity
- aberration models are simplified teaching models rather than full lens-surface ray traces
- thin-lens/paraxial assumptions should be stated where relevant

---

# 20. Latest project files at the time of this handoff

The latest generated version at the end of the previous chat was:

```text
/mnt/data/optics-playground-with-distortion/index.html
```

and:

```text
/mnt/data/optics-playground-with-distortion.zip
```

In a new chat, **do not assume those container paths are still available**.

The user should upload:

1. this Markdown handoff file
2. the latest `index.html` or ZIP

The uploaded `index.html` should be treated as the authoritative source for future development.

---

# 21. Recommended first message to a new ChatGPT chat

The user can say something like:

> I am continuing development of my Optics Playground website. Please read the attached `OPTICS_PLAYGROUND_HANDOFF.md` and use the attached latest `index.html` as the source of truth. Preserve the existing design, physics conventions, Google Analytics, and interaction style. Before making changes, inspect the current code rather than rebuilding it.

---

# 22. Standing instruction for the new chat

**Always check that Google Analytics ID `G-VB4PLZGGJV` remains embedded after every edit.**

Also always run a JavaScript syntax check before returning an updated build.

