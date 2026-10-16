# optics_playground

Interactive web pages for exploring basic ray- and wave-optics concepts, designed for Optics in *Foundations of Physics* at the University of Bath. A single self-contained `index.html` (plus KaTeX and Google Fonts from CDNs) hosted on GitHub Pages.

## Activities (tabs)
- **Waves → Rays** — single-slit diffraction with tunable wavelength (400–700 nm, figure coloured by the light), slit width and screen distance; the schematic screen moves with the distance slider and the slit centre lines up with the intensity plot's centre.
- **Fermat** — Fermat's principle of least time: photons (cats) launched from A at different angles reach B together through a lens whose thickness profile is derived from the equal-OPL condition; animated wavefront; inset of OPL vs launch angle with and without the lens.
- **Refraction** — Snell's law at a plane interface with direction arrows on the incident, refracted and reflected rays; presets; total internal reflection and critical angle.
- **Lens** — build a lens from two surfaces (convex / plano / concave, radii, index, object distance); three principal rays with direction arrows; dimension lines for s₁, s₂ and f; live caption; "finding the image with three rays" guide.
- **Mirror** — spherical concave / convex mirror (paraxial three-ray construction; the mirror symbol's curvature follows R).
- **Off-axis rays** — a collimated bundle at angle θ focuses on the back focal plane at y′ = f tan θ.
- **Eye focus** — object at the front focal plane of a lens; the eye can move axially and stays focused.
- **Microscope** — objective, intermediate image, eyepiece, eye lens and retina; adjustable object distance.
- **Telescope** — Keplerian or Galilean design (toggle), adjustable objective–eyepiece separation, human eye and retina.
- **Aberrations** — spherical, chromatic (white light or single λ), coma, astigmatism (T → S screen slider) and distortion, each against the ideal thin lens.

## Design
Warm editorial design system: ivory paper, navy ink, oxblood accent; Fraunces for headings, IBM Plex Sans for text and figure labels, KaTeX for equations. Every tab uses the same template (figure plate with an italic caption and colour-keyed legend, one row of controls under the figure, formulas / readouts / explanation in the margin) and the same figure conventions (purple / green / navy principal rays, blue glass, purple focal points, green tree objects, direction arrowheads). Canvases render at the device pixel ratio so figures stay sharp when zoomed. Each tab fits one screen at 1280 × 900 and in zoomed browsers.

See `OPTICS_PLAYGROUND_HANDOFF.md` for the full specification and conventions, and `SETUP.md` for GitHub Pages and analytics.

## Google Analytics
GA4 measurement ID `G-VB4PLZGGJV`, embedded in the `<head>` of `index.html` (verified 16 October 2026). Events: `tab_opened`, `simulation_started`, `ray_limit_explored`, `tir_reached`, `critical_angle_reached`, `preset_used` — see `SETUP.md` for the parameters and when each fires.

## Credits
Joe Chen, Centre for Photonics, Department of Physics, University of Bath. Created by ChatGPT GPT-5.6 Sol and Claude Fable 5.1 in 2026.
