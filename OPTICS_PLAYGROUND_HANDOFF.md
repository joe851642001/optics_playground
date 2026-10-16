# Optics Playground — handoff (current as of 16 October 2026, 03:34)

> **Start here.** This file is a running log: the sections below were written as the site evolved, and later sections override earlier ones. The authoritative description of the *current* site is this summary; the dated sections that follow give the detail and the reasoning.

## Current state in one page

- **One file**: `index.html` (plus `.nojekyll`, `README.md`, `SETUP.md`, this file, and `apply_all_tabs.py`, the script that converted the tabs to the editorial template; kept as a record only). GA4 `G-VB4PLZGGJV` in `<head>` (gtag snippet + `gtag('config')`), one `track()` helper, 27 event call sites — audited 16/10/2026, see the table in `SETUP.md`. Every change to the site must keep the GA snippet and the `track()` calls; verify with `grep -c G-VB4PLZGGJV index.html` (expect 2) and `grep -o "track('[a-z_]*'" index.html | sort | uniq -c`.
- **Design system** (section 24 and later): ivory paper `#F6F3EC`, plate white, ink `#1F2A44`, muted `#7A7366`, rule `#D9D2C3`, accent oxblood `#8C2F39` (UI only). Fonts: Fraunces 500 (headings, italic captions), IBM Plex Sans 400/500 (text, labels, canvas), KaTeX for equations. No bold weights other than headings; `.primary` on a button means a *selected state* only.
- **Tab template** (`.ed-*`): the panel is a two-column grid — title, brief and figure column on the left; `aside.ed-side` (320 px) on the right starting level with the title. Figure column = `.ed-plate` (canvas/SVG, white) + italic "Figure." caption + colour-keyed legend + one `.ed-controls` row. Margin = formula(s), `.ed-readout` rows, `.ed-status` sentence, `.ed-howto` block. Refraction is the exception: three columns (figure | stacked controls | Snell's law).
- **Figure conventions**: purple `#7A3FE4` / green `#15A06A` / navy `#1F2A44` for the three principal rays (colour-blind safe), glass stroke `#2F6BD6` with light-blue gradient (`microDrawLens`, `thickness` and `concave` options), focal points purple, green tree objects (`drawArrow` name kept), direction arrowheads on rays, label halos, dimension lines in the Lens tab, no in-canvas legends. Label sizes: Lens 14 px, Waves plot 13 px, Fermat 18–19 px, all other canvases 16 px.
- **Hi-DPI**: all canvases draw in logical coordinates with a dpr-scaled backing store (`canvasSize`, `setCanvasLogicalHeight`); never read `canvas.width/height` for layout.
- **Physics notes**: Lens thickness profile from the sagitta of each surface; Fermat has a Lens / No lens toggle: the shaped lens gives equal OPL for the displayed A→B family, while No lens retains the same family as variational trial paths and shows the straight central path as the unique minimum-time route; Mirror uses a real spherical reflecting curve for the ray geometry: coloured rays terminate on the curve and are reflected about the local radius/normal; the Gaussian image equation remains a paraxial readout; Telescope supports Keplerian (f_eye = +24) and Galilean (f_eye = −24); Waves wavelength 400–700 nm with the figure coloured by `wavelengthCss`.
- **Fit**: every tab fits one screen at 1280 × 900; short viewports (< 800 px) get a compact mode (Lens canvas 300 px tall, scaled canvases elsewhere).

---

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

## Typography (changed 15/10/2026)

Text is set in **Arial** (system font, no web-font import) for all HTML, canvas and SVG text: stack `Arial,"Helvetica Neue",Helvetica,sans-serif`. This matches the look of Optic Sketcher, which the owner likes. Equations are rendered by KaTeX in its own Computer Modern fonts.

**Italic symbols in figures.** In every figure, variable symbols are italic and words are upright (as in LaTeX). Canvas text goes through `fillRich(ctx, str, x, y)`, where `*…*` marks an italic segment, e.g. `fillRich(ctx, 'Air, *n* = 1  (*v* = *c*)', x, y)`; it honours `ctx.textAlign`. `microDrawFocalPoint` labels use the same markup (`'*F′*'`). SVG labels use `<tspan font-style="italic">`. Live status lines written with `innerHTML` use `<i>…</i>` for symbols. Keep this convention for any new label.

The type scale is deliberately flat so sizes do not vary across the page:

```text
h1: 24 px
headings (panel title, card headings): 16.5 px
everything else (body, labels, buttons, tabs, badges, notes, metric values, footer): 14.5 px
metric captions (<small>): 13.5 px
line height: 1.65 everywhere (h1 1.25)
canvas labels: 13 px (600 weight for emphasis); the 🐈 glyph is 25 px
SVG schematic captions: 15 (viewBox units)
```

Only weight 400 is used: no bold anywhere (headings are distinguished by size, emphasis in muted paragraphs by colour via `.muted b{color:var(--text)}`, metric values by colour). Do not add new sizes or weights.

## Equations (added 15/10/2026)

Equations are written in LaTeX and rendered by **KaTeX 0.16.11** (loaded from cdnjs in `<head>`, `defer`). Inline math uses `\( … \)`, display math `\[ … \]`, inside a `.eq` box or the existing equation boxes. `renderAllMath()` runs once KaTeX is available. Live numeric equations (e.g. the Snell's-law substitution) go through `setMath(el, tex, plain)`, which stores the TeX in `data-tex` and falls back to plain text if KaTeX is unavailable. Dynamic status lines written with `innerHTML` stay as plain HTML.

## Type scale (added 15/10/2026)

See the Typography section for the flat type scale. All labels, canvas captions and SVG captions start with a capital letter (single-letter variables such as `n = 1.5` excepted). Spacing is deliberately tight (body padding 16/20 px, card padding 13/14 px, grid gaps 14 px) so that each tab fits in roughly one screen at 1280 px width.

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
- `fermat`
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
2. **Fermat's Principle**
3. **Refraction**
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

Redundancy pass (15/10/2026): each idea is stated once per tab. Removed: the Waves tab's "Red light" box and wavelength metric (replaced by a screen-resolution Δx metric) and its duplicated plot description; the Mirror tab's Concave/Convex preset buttons (the Mirror type select does this); the Off-Axis "What to look for" paragraph that repeated the subtitle; two of three overlapping Eye Focus paragraphs; the "Objective/Eyepiece fixed at …" lines in Microscope and Telescope (already in the metric cards); and the Aberrations control notes that repeated the metric note (spherical, coma, astigmatism; distortion shortened). Avoid reintroducing text that restates the subtitle, the badge, the metric note or the status line.

Current approximate canvas/frame sizes:

- Fermat canvas: `860 × 400`
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

No preset buttons and no regime badge (removed 15/10/2026 at the owner's request); the status line below the metrics still describes the regime. The schematic shows only: Incident light (label on the arrow), Single slit, Slit width a (dimension arrow), Screen distance L, Screen →. No beam arrow after the slit.

User prefers small schematic arrowheads.

Current wave metrics were moved into unused left-column space rather than a full-width strip.

Alignment rule (15/10/2026): the schematic SVG ( `preserveAspectRatio="xMidYMid meet"`) and the screen canvas (330 × 440) (viewBox 520 × 440, `width:100%; height:auto`, so it fills its panel at any page width; canvas 330 × 440 in a 272 px column) are kept the same rendered height by `syncWaveCanvasHeight()`, which sets the canvas's internal height from the schematic's rendered height on every update, on resize and when the tab is shown. The plot's padding is computed so its zero line sits at exactly 218/440 of the canvas height whatever that height is. Both panels have identical headers, and the slit axis sits at y = 218 in both (canvas: padT + plotH/2). A red dashed "ray-optics centre" line runs from the slit across the schematic and continues in the plot. The slit bar is 14 units wide, so the slit centre lines up exactly with the "Ray-optics centre" line of the plot (the red beam arrow itself was removed). Keep these numbers in step if either drawing changes. The regime status line was removed; the four metric cards and the "Tuning knobs" heading were removed; the controls (wavelength, slit width, screen distance) sit in one full-width card directly under the drawings, three columns; all explanatory text lives in the "Diffraction pattern" card in the right column. The tab fits one screen (~700 px panel height).

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

The figure is a **visibly curved spherical mirror** using the textbook **paraxial three-principal-ray construction**. The mirror profile remains curved, but the small spherical sag at the ray heights is neglected when applying the principal-ray rules (equivalently, the rays use the tangent plane through the mirror vertex). This makes the textbook rules exact on the diagram: the parallel ray passes through `F`, the focal ray reflects parallel, and all three rays locate the same Gaussian image (or their dashed back-extensions meet at the virtual image).

Controls:

- concave / convex (select)
- `|R|`
- object distance `s₁`

Paraxial readouts:

\[
f=\frac{R}{2}
\]

\[
\frac{1}{f}=\frac{1}{s_1}+\frac{1}{s_2}
\]

\[
m=-\frac{s_2}{s_1}
\]

Sign convention: concave mirrors have `R,f > 0`; convex mirrors have `R,f < 0`; a real object has `s₁ > 0`; a real image has `s₂ > 0`, while a virtual image has `s₂ < 0`.

Current curved-mirror principal-ray model:

- The blue mirror remains visibly curved for both concave and convex cases; never replace it with a visibly flat mirror.
- The construction itself is **paraxial**: ray intercepts use the tangent plane through the mirror vertex (`x = 0`). The spherical sag at the small model ray heights is second order and is intentionally neglected when applying the textbook ray rules.
- The visible mirror curve is drawn from the spherical sag with a mild horizontal exaggeration so its curvature remains obvious while the paraxial intercept plane stays visually close to the blue surface.
- Purple ray: incident parallel to the optical axis, reflected through `F` for a concave mirror (or reflected as if from virtual `F` for a convex mirror). The `F` marker must lie exactly on the purple reflected ray/back-extension.
- Green ray: directed through (or toward) `F`, then reflected parallel to the optical axis.
- Navy ray: directed through (or toward) `C`, so it retraces its path in the paraxial construction. Near the degenerate `s₁=|R|` case, use the vertex ray as the stable limiting third construction.
- The three rays meet exactly at the Gaussian image for `s₂>0`; for `s₂<0`, their dashed back-extensions meet exactly at the virtual image.
- At `s₁=f` for a concave mirror, the image is at infinity and all three reflected rays are parallel; the green focal ray uses a stable limiting construction because the literal focal ray would strike outside the finite drawing aperture.
- Keep `C` marked on the axis as the centre of curvature.
- Do not reintroduce exact finite-aperture spherical ray tracing in this tab: spherical aberration would make the rays miss the common Gaussian image and undermine the intended first-year principal-ray construction.

Object/image drawing:

- Object and image are green tree drawings.
- The optical object height is kept paraxial (`min(30 mm, 0.16|R|)`), while a separate vertical drawing scale renders the object tree at about `96 px` high. This preserves the large, readable tree requested by the owner without pushing the ray construction outside the paraxial regime.
- The image-tree height is `m` times the displayed object-tree height, so the image remains visually consistent with the magnification readout.
- The mirror vertex keeps the small blue dot but has **no `V` text label**.
- `Object`, `Image` / `Virtual image`, `F`, and `C` labels use 16 px IBM Plex Sans, matching the other ray-diagram tabs.

Visual colours follow the site convention: purple `#7A3FE4`, green `#15A06A`, navy `#1F2A44`; the reflecting surface is glass blue `#2F6BD6`.

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
Joe Chen. Centre for Photonics, Department of Physics, University of Bath. Created by ChatGPT GPT-5.6 Sol and Claude Fable 5.1 in 2026.
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


---

# 23. Fermat's Principle tab (added 15/10/2026; Lens / No lens comparison added 16/10/2026)

Tab id: `fermat` (`panel-fermat`, canvas `#fermatCanvas`, 860 × 400). Keep the tab compact enough to fit one screen at 1280 × 900. The controls row is now four groups: path-angle slider | time slider | Optical element (`Lens` / `No lens`) | Play/Restart. The right column holds the four live readouts, one live status sentence and the "What to look for" explanation.

### Teaching goal

The tab now compares two related Fermat-principle ideas without changing the displayed A→B path family:

1. **Lens mode** — a specially shaped lens equalises the optical path length of all displayed paths from A to B, so the cats arrive at B together.
2. **No lens mode** — the lens disappears but the same A→B family is retained as **variational trial paths**. In homogeneous air, the straight central path (`θ = 0`) has the minimum OPL and therefore reaches B first. The kinked off-axis paths are deliberately comparison paths, **not physical free-space rays**; this distinction is stated on the page.

This is important: do not describe the kinked off-axis no-lens paths as rays that spontaneously bend in air. The true physical ray from A to B in uniform air is the straight central line.

### Fixed geometry and lens model

```text
A at x = -80 mm, B at x = +80 mm
lens / trial-path centre plane at x = 0
n = 1.5 in lens mode
centre thickness t(0) = 12 mm
half-aperture / trial-path height limit = 19 mm
f = 40 mm for the lens conjugate pair
c = 299.792458 mm/ns
```

In Lens mode, each ray is drawn horizontally through the glass. The lens thickness profile `t(y)` is solved by bisection so that

```text
sqrt((s1 - t/2)^2 + y^2) + n t + sqrt((s2 - t/2)^2 + y^2)
    = OPL0
    = s1 + s2 + (n - 1)t(0)
    = 166 mm
```

for every displayed height. Therefore every Lens-mode path has identical OPL and identical arrival time.

In No lens mode, the comparison path at centre-plane height `y` is

```text
A (-80,0) -> (0,y) -> B (+80,0)
OPL_air(y) = sqrt(80^2 + y^2) + sqrt(80^2 + y^2)
```

so the central path has `OPL = 160 mm`, and every non-zero `|y|` is longer. For the path-angle control, `y = 80 tan θ` (clamped to the displayed ±19 mm family). At `θ = 8°`, for example, the no-lens trial path is about `1.57 mm` longer than the central path, corresponding to about `0.00525 ns` extra travel time.

### Controls and animation

- path angle `θ`: −13° to +13°
- time scrubber with Play/Pause and Restart; auto-plays and loops
- `Lens` / `No lens` state buttons (`#fermatLensBtn`, `#fermatNoLensBtn`)
- changing optical-element mode resets the displayed trip to the start but preserves whether playback was running or paused
- `simulation_started` remains the only Fermat GA event (`activity: fermat`); no extra analytics event was added for the toggle

The animation uses a common elapsed time for all displayed cats. In Lens mode all arrive together. In No lens mode the timeline extends to the longest displayed trial path, so the green central cat visibly reaches B before the purple off-axis cats and waits there while they finish.

### Visuals

- green on-axis reference path
- purple selected path plus a faint mirror path at `−θ`
- 🐈 at the head of each travelled path
- shaped blue lens, focal points F/F′ and orange physical wavefront **only in Lens mode**
- No lens mode removes the lens and focal points completely; bottom-right canvas note reads `No lens: n = 1 everywhere`
- A/B remain fixed; B is labelled `Image point` in Lens mode and `Point B` in No lens mode
- inset remains at top-right and always shows both OPL curves: blue flat Lens curve and dark No-lens minimum curve; the active mode is visually emphasised and the purple marker moves onto the active curve
- the orange wavefront legend item is hidden in No lens mode because the kinked trial-path family is not a physical free-space wavefront

### Live readouts and wording

Readouts remain: path angle, air / glass path, OPL (including Δ relative to the central path), and arrival time at B. In Lens mode ΔOPL is zero. In No lens mode the selected off-axis path reports a positive ΔOPL and corresponding later arrival time.

The page title is now **“Fermat's principle: what changes when the lens is removed”**. The subtitle and status explicitly state that the no-lens central path is the minimum-time route. Keep the phrase **trial paths** in the no-lens explanation to avoid implying unphysical refraction in empty space.



## Refraction tab layout (15/10/2026)

No subtitle, no mode badge, no live numeric Snell substitution. Under the readouts, the Snell equation sits left-aligned with the live explanation text beside it. The right column has the Controls card (three sliders plus a 2-column button grid: Air → glass, Water → air, Glass → air, Swap media, and a full-width "Try total internal reflection"; the Diamond preset was removed) only; the Mini challenge card and its critical-angle button were removed (the `critical_angle_reached` event still fires when the slider reaches the critical angle). The equation row reads "Snell's law: [equation] [live explanation]". The tab fits one screen.


## Lens tab layout (15/10/2026)

The canvas caption is a colour-keyed legend of the three principal rays (purple: parallel ray → through F′; green: centre ray, undeviated; black: ray through F → parallel), drawn with `fillRich`/`richWidth`; it replaces the old "Thin-lens approximation…" caption.

Equation boxes are titled "Lens-maker formula" and "Gaussian lens formula". The Signed R₁/R₂ metric cards and the sign-convention note were removed; only Focal length f and Image distance s₂ remain, as one-line pills. The equation boxes are compact rows (title left, formula right), and the preset buttons are a 2 × 2 grid of small buttons; the "Lens surfaces" heading was removed. The live status line sits in the right column under the controls card. Panel height ≈ 730 px at 1280 × 900.


---

# 24. Editorial redesign (started 15/10/2026)

The site is being moved to a "warm editorial" design system, one tab at a time. The **Lens tab is the reference implementation**; copy its structure when converting the others.

Tokens (CSS `:root`): paper `--bg #F6F3EC`, plate `--card #FBF9F4`, ink `--text #1F2A44`, muted `#7A7366`, rule `--border #D9D2C3`, accent (oxblood) `--accent #8C2F39`. Optical colours (colour-blind safe: no red next to green; the owner wants them bright, not muted): `--ray1 #7A3FE4` purple (parallel ray), `--ray2 #15A06A` green (centre ray), `--ray3 #1F2A44` navy (focal ray), glass stroke `#2F6BD6` with a light-blue gradient fill, focal points purple. The figure plate is white (`.ed-plate`, canvas paper `#FFFFFF`, halo colour white) so the colours pop against the ivory page. The oxblood accent is for the UI only (active tab, status rule), never for rays. Typography: Fraunces 500 (headings, captions in italic 400) and IBM Plex Sans 400/500 (everything else, including canvas labels at 13.5 px). Equations stay in KaTeX. No bold, no cards-in-cards, no badges.

Tab template (`.ed-*` classes): `h2.ed-title` + `p.ed-sub`; `.ed-layout` = figure column (`.ed-plate` canvas 860 × 390, `.ed-caption` "Figure. …" italic serif, `.ed-legend` colour-keyed swatches, then `.ed-controls` as ONE slim row of four groups directly under the figure: Left surface | Right surface | Glass and object | Presets, Fraunces `h4` headings, selects/ranges, 2×2 `.pz` preset grid) and `aside.ed-side` 320 px holding the formulas (serif `h3` + display equations), the `.ed-status` conclusion, and an `.ed-howto` block ("Finding the image with three rays": a numbered, colour-swatched description of the three principal rays and the virtual-image / diverging-lens cases). There are no readout cards: the figure's dimension lines show f, s₁, s₂ (the `#lensFocalMetric/#lensImageMetric` spans are kept hidden for the JS). Principle: controls sit next to what they control; the margin is reference only. The canvas is always drawn at its true proportions (never squashed by CSS). On short viewports (`window.innerHeight < 800`) the Lens canvas is re-created 300 px tall instead of 390 (`lensCanvasHeightForViewport`, redrawn on resize, with lens half-height and object height derived from H), and a `@media (max-height:800px)` block tightens spacing and type, so the tab fits one screen even in a zoomed browser (verified at 1335 × 690, 1280 × 900 and 1790 × 830).

Figure conventions: paper background, dashed axis in `#C9C2B4`, object and image as the green tree with a brown trunk used in the Mirror tab (`drawArrow` — kept its name — draws it; negative height = inverted; a virtual image is drawn at 55 % opacity). The owner prefers the tree to a bare arrow, no in-canvas legend (legend is HTML), lens plane as a faint dotted line, labels in Plex 16.5 px with a paper-coloured halo (`haloText`) so they stay legible over rays, a small arrowhead on each incoming ray (`rayArrowhead`) to show the direction of light, and dimension lines below the axis for s₁, s₂ and f (`dimensionLine`, label placed under the bar so short bars stay visible; rows at H−30, H−56, H−82) so the figure quotes the quantities used in the formulas. The lens profile is derived from the surface radii (`surfaceBulge` uses the real sagitta, exaggerated for legibility); the edge half-thickness is computed per frame so that concave surfaces never cross at the centre (a quadratic Bézier's midpoint lies half-way to its control point, so the edge grows by half the inward bulge). The radius sliders visibly change the shape. Virtual-image labels are placed to the left of the dashed arrow. The caption is written live by JS (`#lensCaption`). Reuse these helpers in every other figure.

Masthead: site name in Fraunces on the left, tabs as text links on the right (active = oxblood underline).

**All ten tabs now use the `.ed-*` template** (converted 15/10/2026 by `apply_all_tabs.py`, kept in the working folder as a record). Per tab: `h2.ed-title`, `p.ed-sub`, figure plate (canvas, or the SVG for Refraction, or the two-panel SVG+canvas for Waves), italic "Figure." caption, optional colour-keyed legend, one controls row (`.ed-controls`, column widths set inline per tab), and a 320 px `aside.ed-side` with the formula(s), `.ed-readout` rows, the live `.ed-status` sentence and an `.ed-howto` block. Old badge elements are kept as hidden spans (`*StatusBadge`) because the JS still writes to them; the Aberrations tab uses its badge as the side heading. All old canvas colours were remapped to the editorial palette (purple #7A3FE4, green #15A06A, navy #1F2A44, glass blue #2F6BD6, red #E03E3E only where red light or TIR is meant, axis/grid #C9C2B4/#DDD6C8, muted text #7A7366). Off-axis bundle rays are all purple; Refraction rays use the CSS `--ray1/2/3` tokens (incident purple, refracted green, reflected navy dashed).

Short viewports: the Lens canvas is redrawn at 300 px; other canvases are scaled down by CSS keeping their aspect (`.ed-plate canvas:not(#lensCanvas)` under `@media (max-height:800px)`); the Waves panels are 280 px and the Refraction SVG 320 px tall there.

Button convention: the dark `.primary` style is a *state* (the selected mode in the Aberrations tab), never a decoration. Preset/action buttons (On axis, Try TIR, Pause) have no `primary` class.

`microDrawLens` (used by Off-axis, Eye focus, Microscope, Telescope, Aberrations) now draws the same glass look as the Lens tab: thin edge, two arc surfaces, blue stroke with a light-blue gradient; the eye lens (colour #1F2A44) gets a grey-navy gradient instead.

Lens heights (half-height px) chosen to cover every drawn ray: Microscope objective 72 / eyepiece 168 (rays reach ~150 px below the axis at the extremes); Telescope objective 118 / eyepiece 90; Aberrations lens = half the max aperture in px + 14. `microDrawLens` keeps the glass slim (bulge 8–14 px) regardless of height; labels sit just above each lens.

Waves schematic: the screen (dashed line `#schematicScreen`, label `#schematicScreenLabel` below it, the red centre line `#schematicAxis` and the `Distance L` dimension) moves with the screen-distance slider: x = 365 + (L − 0.2)/2.8 × 145 in viewBox units.

Waves tab: wavelength is now a slider (400–700 nm). The figure is coloured by the chosen wavelength (`wavelengthCss`), so blue light gives a blue curve/arrow, red light a red one.

Telescope tab (16/10/2026): a Design toggle (`#telKeplerBtn` / `#telGalileoBtn`, state buttons) switches `telescopeState.type` between `keplerian` (f_eye = +24 mm, normal L = 144 mm, M = −5, inverted) and `galilean` (f_eye = −24 mm, normal L = 96 mm, M = +5, upright). `telEyepieceFocal()` and `telNormalSeparation()` replace the old constants; the slider is re-ranged on each switch: normal ± 12 mm (Keplerian) or ± 6 mm (Galilean, which defocuses twice as fast). The eye lens and retina are 152 px half-height, and the eye lens is drawn at 0.55× thickness (`microDrawLens(..., concave, thickness)`), so the rays stay inside a slim eye at every slider extreme. `microDrawLens(..., concave=true)` draws the diverging eyepiece as a biconcave lens. In the Galilean case the objective's would-be intermediate image is drawn translucent with the note "(would-be image: never forms)". The figure caption `#telescopeCaption` is set live. Events: `preset_used` with preset `keplerian` / `galilean`.

Fermat inset (16/10/2026): 360 × 150 px at the top right of the canvas; dark axes, blue 3 px "with lens" line, dark navy dashed "no lens" curve, 6 px purple marker. Waves plot: the small "Screen" label above the plot was removed (the panel header already says it).

Refraction tab layout (16/10/2026): THREE columns (`.ed-layout.ed-layout-3`, 1fr / 250 px / 250 px): figure (plate, caption, legend) | controls stacked (`.ed-col2`: Medium 1, Medium 2, Incidence + TIR button, Presets as single-column buttons) | Snell's law (`.ed-col3`: formula, readouts, live explanation). The SVG fills its plate. Below 1100 px the third column drops under the first two. Panel ≈ 665 px tall at 1280 × 900.

Refraction SVG: each ray carries a direction arrowhead (`#incidentArrow`, `#refractedArrow`, `#reflectedArrow` polygons, positioned by `placeArrow()` at 55 % along the ray; the refracted arrow is hidden under TIR).

Mirror tab (16/10/2026, superseded later the same day): the earlier vertex-plane construction was replaced after review. The current version traces rays on the actual spherical curve; see the final note below.

Canvas label sizes (16/10/2026, tuned per tab at the owner's request): Lens 16 px (Object/Image and dimension labels 15 px); Off-axis and Eye focus 16 px (matching Microscope/Telescope/Aberrations); Waves plot 13 px with the schematic SVG at 19 viewBox units; Fermat 18–19 px (inset title 20 px, inset text 18 px); all other canvases 16 px. The Refraction SVG is unchanged. The Waves plot legend shows only the intensity curve (the 'Fixed 0.20 mm resolution' entry was removed; the pale band itself still draws).

## Hi-DPI canvases (16/10/2026)

All canvases are drawn in a fixed logical coordinate system (their HTML `width`/`height`), while the backing store is scaled by `devicePixelRatio` (capped at 3) so lines and text stay sharp on HiDPI screens and zoomed browsers. `CANVAS_LOGICAL[id]` holds the logical size; every draw routine starts with `const { W, H } = canvasSize(canvas, ctx)` (sets the backing size and `ctx.setTransform(dpr,…)`). Never read `canvas.width/height` for layout; use `canvasSize`. Canvases whose logical height changes (Lens on short viewports, Waves to match the schematic) go through `setCanvasLogicalHeight()`. The resize handler redraws every figure when the zoom level (dpr) changes. Lens labels are 14 px (Object/Image labels 13 px — set inside `drawArrow`, which has its own font line — dimension labels 13.5 px) with a 3.5 px halo.

## Mirror physics/rendering correction (16/10/2026, superseded)

An intermediate version temporarily drew an effective flat reflecting plane with the curve only as a visual cue. **Do not restore that model.** It was superseded later the same day by the true curved-surface model below.


## Mirror curved-surface correction (16/10/2026, superseded)

The Mirror figure must visibly and physically be a **curved spherical mirror**, not a flat effective plane. The old 01:33-era file was used only as a visual reference for the curved profile; its rays still terminated at a separate vertex plane, which was not retained.

Current model:

- The blue mirror line is a true circular arc in the same isotropic x/y scale as the rays.
- Concave: sphere centre `C` lies on the object side (left) and the reflecting cap is the right-hand branch; convex is the opposite.
- Every coloured incident ray terminates on that curved arc.
- Reflection uses the exact vector law `d_out = d_in - 2(d_in·n)n`, where `n` is the local radius/normal through `C`.
- Three sample rays are shown: a parallel incident ray, a vertex ray, and an oblique ray. They are no longer falsely forced to obey ideal principal-ray rules away from the axis.
- `f = R/2`, the Gaussian mirror equation and `m = -s2/s1` remain as **paraxial** readouts. The drawn image tree is explicitly labelled “Paraxial image”. Exact spherical rays may miss it slightly at finite height, correctly showing spherical aberration.
- For virtual images, reflected rays are back-extended with dashed lines behind the curved mirror.
- Keep GA4 and all existing tracking calls unchanged.

- Mirror object tree is enlarged for legibility: its nominal height is `1.9 ×` the previous base size, capped at `0.96 ×` the spherical aperture so the object-tip ray still lands on the physical mirror. The paraxial image height still follows the calculated magnification exactly.
- The mirror vertex dot is retained but its `V` text label has been removed. Remaining Mirror figure labels (`Object`, `Paraxial image` / `Virtual paraxial image`, `F`, `C`) use 16 px IBM Plex Sans, matching the label scale used across the other ray-diagram tabs.


## Fermat Lens / No lens toggle (16/10/2026, final)

The Fermat tab now has an `Optical element` mode switch. `Lens` preserves the equal-OPL lens animation. `No lens` removes all lens/focal-point graphics but keeps the same A→B comparison family as trial paths. At a common elapsed time the straight green path reaches B first; off-axis purple trial paths arrive later according to their longer geometric path. The inset highlights whichever model is active. Do not turn the no-lens off-axis comparison paths into physical bent rays in air; they are variational trial paths used to demonstrate the minimum-time principle.

## Mirror principal-ray convergence correction (16/10/2026, final)

The Mirror tab was changed back to a **paraxial principal-ray teaching construction while retaining the visibly curved spherical mirror**. The exact finite-aperture spherical-reflection version was not appropriate here because spherical aberration made the three coloured rays miss the Gaussian image, which conflicts with the purpose of a principal-ray diagram.

Current required behaviour:

- Keep the blue reflecting profile visibly curved for both concave and convex mirrors.
- Use the Gaussian mirror relations `f=R/2`, `1/f=1/s₁+1/s₂`, `m=-s₂/s₁`.
- Draw three colour-coded principal construction rays from the object tip. Their incident portions meet the visible curved arc.
- For `s₂>0`, all three reflected rays must pass through the same real image tip.
- For `s₂<0`, all three dashed back-extensions must pass through the same virtual image tip.
- At the concave focal condition `s₁=f`, the reflected rays are parallel and the image readout is infinity.
- The object tree remains enlarged for visibility (`1.9 ×` base, aperture-capped), the vertex has a dot but no `V` text label, and Mirror labels remain 16 px.
- Do **not** restore either of the two superseded variants: (1) the visibly flat effective mirror, or (2) exact finite-aperture spherical ray tracing that shows aberration instead of a common principal-ray image.
- Keep GA4 and all existing tracking calls unchanged.


## Mirror focal-point alignment correction (16/10/2026, current)

The final Mirror correction fixes the purple principal ray so that the paraxial focal point `F` lies **exactly on the purple reflected ray** (or on its dashed back-extension for a convex mirror). The previous curved-contact construction forced all rays to the Gaussian image from points on the finite-sag spherical arc; with the deliberately large object this made the purple line miss `F`, which is inconsistent with the textbook principal-ray rule.

Current implementation therefore uses the standard tangent-plane paraxial construction while retaining a clearly curved blue mirror profile. This gives an internally consistent teaching diagram across concave and convex modes: purple through `F`, green reflected parallel, navy through/toward `C` (with a vertex fallback only at the degenerate `s₁=|R|` case), and all three meeting at the Gaussian image (or its virtual back-intersection).
