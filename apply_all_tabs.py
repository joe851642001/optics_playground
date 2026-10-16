import re
p = '/home/claude/op/index.html'
s = open(p).read()

def rep(a, b, c=1):
    global s
    n = s.count(a)
    assert n == c, (n, a[:90])
    s = s.replace(a, b)

# ------------------------------------------------------------------ colour palette for every figure
# (applied to the JS and the inline SVGs; the new tokens are untouched)
cmap = {
    '#8b5cf6': '#7A3FE4', '#7b61ff': '#7A3FE4',
    '#117a55': '#15A06A', '#16a34a': '#15A06A', '#0f766e': '#15A06A',
    '#315efb': '#2F6BD6', '#2563eb': '#2F6BD6',
    '#172033': '#1F2A44', '#111111': '#1F2A44', '#111827': '#1F2A44', '#344054': '#1F2A44', '#475467': '#1F2A44',
    '#667085': '#7A7366', '#98a2b3': '#C9C2B4', '#c8cfda': '#DDD6C8', '#d9dee8': '#DDD6C8', '#e4e7ec': '#EAE4D8',
    '#e1e6ef': '#EAE4D8', '#e8ecf3': '#EAE4D8', '#fbfcfe': '#FFFFFF',
    '#d64545': '#E03E3E', '#ef4444': '#E03E3E', '#dc2626': '#E03E3E',
    '#b54708': '#C2570B',
    'rgba(49,94,251,': 'rgba(90,150,255,', 'rgba(139,92,246,': 'rgba(122,63,228,', 'rgba(123,97,255,': 'rgba(122,63,228,',
    'rgba(17,122,85,': 'rgba(21,160,106,',
}
head_end = s.find('</style>')
head, body = s[:head_end], s[head_end:]
for a, b in cmap.items():
    body = body.replace(a, b)
s = head + body

# ------------------------------------------------------------------ helpers
def panel(name, title, sub, plate, caption, legend, controls_cols, controls, side, hidden=True, caption_id=None):
    cap_id = f' id="{caption_id}"' if caption_id else ''
    leg = ''
    if legend:
        leg = '        <div class="ed-legend">\n' + ''.join(
            f'          <span><i class="sw" style="background:{c}{";height:0;border-top:2px dashed " + c if dashed else ""}"></i>{t}</span>\n'
            for c, t, dashed in legend) + '        </div>\n'
    return f'''  <section id="panel-{name}" class="tab-panel ed" role="tabpanel" aria-labelledby="tab-{name}"{' hidden' if hidden else ''}>
    <h2 class="ed-title">{title}</h2>
    <p class="ed-sub">{sub}</p>
    <div class="ed-layout">
      <div>
        <div class="ed-plate">
{plate}
        </div>
        <p class="ed-caption"><b>Figure.</b> <span{cap_id}>{caption}</span></p>
{leg}        <div class="ed-controls" style="grid-template-columns:{controls_cols}">
{controls}
        </div>
      </div>
      <aside class="ed-side">
{side}
      </aside>
    </div>
  </section>

'''

def grab(start, end_marker='<section id="panel-'):
    i = s.find(start.strip())
    assert i >= 0, start
    # include leading indentation on that line
    i = s.rfind('\n', 0, i) + 1
    j = s.find(end_marker, i + 10)
    if j < 0:
        j = s.find('<footer>')
    return i, j

def slider(id_, label, value_id, value, mn, mx, step):
    return f'''            <label for="{id_}"><span>{label}</span><b id="{value_id}">{value}</b></label>
            <input id="{id_}" type="range" min="{mn}" max="{mx}" step="{step}" value="{value.split(' ')[0] if False else ''}">'''

# ------------------------------------------------------------------ 1. Waves → Rays
i, j = grab('  <section id="panel-wave-ray"')
old = s[i:j]
svg = re.search(r'<svg id="singleSlitSchematic".*?</svg>', old, re.S).group(0)
plate = f'''          <div class="wave-visuals ed-two">
            <div class="wave-left-panel">
              <div class="ed-panel-h">Single-slit experiment</div>
              {svg}
            </div>
            <div class="wave-right-panel">
              <div class="ed-panel-h">Screen intensity pattern</div>
              <div class="wave-canvas-wrap">
                <canvas id="waveCanvas" width="330" height="440" role="img" aria-label="Single-slit diffraction intensity on a screen plotted against vertical screen position."></canvas>
              </div>
            </div>
          </div>'''
controls = '''          <div>
            <h4>Light</h4>
            <label><span>Wavelength <i>λ</i></span><b id="wavelengthValue">650 nm</b></label>
            <div class="ed-fixed">fixed, red</div>
          </div>
          <div>
            <h4>Slit</h4>
            <label for="slitWidthRange"><span>Width <i>a</i></span><b id="slitWidthValue">100 μm</b></label>
            <input id="slitWidthRange" type="range" min="1" max="2000" step="1" value="100">
          </div>
          <div>
            <h4>Screen</h4>
            <label for="screenDistanceRange"><span>Distance <i>L</i></span><b id="screenDistanceValue">1.00 m</b></label>
            <input id="screenDistanceRange" type="range" min="0.2" max="3.0" step="0.05" value="1.00">
          </div>'''
side = '''        <div class="block">
          <h3>Diffraction pattern</h3>
          <p class="ed-text">Light passes through a single slit of width \\(a\\) and lands on a screen at distance \\(L\\); the right-hand panel is that screen. The intensity as a function of screen position \\(x\\) is</p>
          \\[ I(x) \\propto \\operatorname{sinc}^2\\!\\left(\\frac{\\pi a x}{\\lambda L}\\right) \\]
          <p class="ed-text">with the first minimum at \\(|x_1| \\approx L\\lambda/a\\), so a wider slit gives a narrower pattern.</p>
        </div>
        <div class="ed-howto">
          <h3>Why this becomes ray optics</h3>
          <p>When the slit is much wider than the wavelength, the diffraction width \\(2L\\lambda/a\\) becomes tiny compared with the screen resolution \\(\\Delta x\\). The wave is still there, but the straight-through beam is then a very good approximation.</p>
        </div>'''
new = panel('wave-ray', 'From wave optics to ray optics',
            'A single-slit experiment at fixed wavelength. Make the slit wider and watch diffraction shrink toward the straight-through ray-optics limit.',
            plate, 'Red light passes a single slit of width <i>a</i> (left) and reaches a screen at distance <i>L</i> (right), where the intensity is plotted against position on the screen. The slit centre and the centre of the pattern are on the same line.',
            None, '1fr 1.4fr 1.4fr', controls, side, hidden=False)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 2. Fermat
i, j = grab('  <section id="panel-fermat"')
plate = '''          <canvas id="fermatCanvas" width="860" height="400" role="img" aria-label="Point source A on the left, a biconvex lens in the middle and image point B on the right. Cats ride at the head of each ray and sit on the wavefront; all of them arrive at B at the same time."></canvas>'''
controls = '''          <div>
            <h4>Launch direction</h4>
            <label for="fermatAngle"><span>Ray angle from A, <i>θ</i></span><b id="fermatAngleValue">+8.0°</b></label>
            <input id="fermatAngle" type="range" min="-13" max="13" step="0.5" value="8">
          </div>
          <div>
            <h4>Time</h4>
            <label for="fermatTime"><span>Elapsed</span><b id="fermatTimeValue">0.000 ns</b></label>
            <input id="fermatTime" type="range" min="0" max="1000" step="1" value="0">
          </div>
          <div>
            <h4>Playback</h4>
            <div class="pz">
              <button id="fermatPlayBtn" class="primary">Pause</button>
              <button id="fermatRestartBtn">Restart</button>
            </div>
          </div>'''
side = '''        <div class="block">
          <h3>Optical path length</h3>
          \\[ \\mathrm{OPL} = \\sum_i n_i L_i, \\qquad t = \\frac{\\mathrm{OPL}}{c} \\]
          <div class="ed-readout"><span>Ray angle <i>θ</i> at A</span><b id="fermatAngleMetric">+8.0°</b></div>
          <div class="ed-readout"><span>Air / glass path</span><b id="fermatGeoMetric">— / — mm</b></div>
          <div class="ed-readout"><span>OPL</span><b id="fermatOplMetric">— mm</b></div>
          <div class="ed-readout"><span>Arrival time at B</span><b id="fermatTimeMetric">— ns</b></div>
        </div>
        <div class="ed-howto">
          <h3>What to look for</h3>
          <p>The green on-axis cat is the reference: it reaches the glass first, then crawls through the thickest part of the lens at \\(v = c/n\\). The purple cat takes a longer air path at full speed \\(c\\) and crosses only a thin sliver of glass.</p>
          <p>The longer air path and the thinner glass cancel exactly, so \\(d(\\mathrm{OPL})/d\\theta = 0\\): equal OPL means equal time. The orange wavefront stays perpendicular to every ray, all cats sit on it, and they meet at B together.</p>
        </div>'''
new = panel('fermat', 'Fermat\'s principle: every ray from A to B takes the same time',
            'Launch a photon (cat) from A in any direction: fast in air, slow in glass, yet every one reaches B at the same instant because \\(\\mathrm{OPL} = \\sum n L\\) is the same for every ray.',
            plate, 'Photons launched from A at different angles are shown at equal times; the lens thickness is chosen so that every path from A to B has the same optical length.',
            [('#15A06A', 'On-axis reference ray', False), ('#7A3FE4', 'Chosen ray at angle <i>θ</i> (and its mirror)', False), ('#f59e0b', 'Wavefront: equal OPL from A', False)],
            '1.3fr 1.3fr 1fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 3. Refraction
i, j = grab('  <section id="panel-refraction"')
old = s[i:j]
svg = re.search(r'<svg id="raySvg".*?</svg>', old, re.S).group(0)
plate = '          ' + svg
controls = '''          <div>
            <h4>Medium 1</h4>
            <label for="n1Range"><span>Index <i>n</i>₁</span><b id="n1Value">1.00</b></label>
            <input id="n1Range" type="range" min="1" max="2.6" step="0.01" value="1">
          </div>
          <div>
            <h4>Medium 2</h4>
            <label for="n2Range"><span>Index <i>n</i>₂</span><b id="n2Value">1.50</b></label>
            <input id="n2Range" type="range" min="1" max="2.6" step="0.01" value="1.5">
          </div>
          <div>
            <h4>Incidence</h4>
            <label for="angleRange"><span>Angle <i>θ</i>₁</span><b id="angleValue">30.0°</b></label>
            <input id="angleRange" type="range" min="0" max="89" step="0.1" value="30">
          </div>
          <div>
            <h4>Presets</h4>
            <div class="pz presets refraction-presets">
              <button data-preset="air-glass">Air → glass</button>
              <button data-preset="water-air">Water → air</button>
              <button data-preset="glass-air">Glass → air</button>
              <button id="swapBtn">Swap media</button>
              <button id="tirBtn" class="primary">Try total internal reflection</button>
            </div>
          </div>'''
side = '''        <div class="block">
          <h3>Snell's law</h3>
          \\[ n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2 \\]
          <div class="ed-readout"><span>Incident angle <i>θ</i>₁</span><b id="incidentReadout">30.0°</b></div>
          <div class="ed-readout"><span>Refracted angle <i>θ</i>₂</span><b id="refractReadout">19.5°</b></div>
          <div class="ed-readout"><span>Critical angle</span><b id="criticalReadout">—</b></div>
        </div>
        <p id="explanation" class="ed-status">Light enters a higher-index medium, so it bends toward the normal.</p>'''
new = panel('refraction', 'Refraction at a plane interface',
            'Change the two refractive indices and the angle of incidence; watch the refracted ray bend, and find the critical angle for total internal reflection.',
            plate, 'A ray in medium 1 meets a plane interface with medium 2. Angles are measured from the normal; the dashed line continues the incident ray.',
            [('#2F6BD6', 'Incident ray', False), ('#E03E3E', 'Refracted ray', False), ('#7A3FE4', 'Reflected ray', False)],
            '1fr 1fr 1fr 1.3fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 4. Mirror
i, j = grab('  <section id="panel-mirror"')
plate = '''          <canvas id="mirrorCanvas" width="860" height="400" role="img" aria-label="Interactive spherical-mirror ray diagram with object tree, image tree and principal rays."></canvas>'''
controls = '''          <div>
            <h4>Mirror</h4>
            <select id="mirrorType" aria-label="Mirror type">
              <option value="concave" selected>Concave</option>
              <option value="convex">Convex</option>
            </select>
          </div>
          <div>
            <h4>Curvature</h4>
            <label for="mirrorRadiusRange"><span>Radius |<i>R</i>|</span><b id="mirrorRadiusValue">160 mm</b></label>
            <input id="mirrorRadiusRange" type="range" min="60" max="500" step="5" value="160">
          </div>
          <div>
            <h4>Object</h4>
            <label for="mirrorObjectDistanceRange"><span>Distance <i>s</i>₁</span><b id="mirrorObjectDistanceValue">300 mm</b></label>
            <input id="mirrorObjectDistanceRange" type="range" min="80" max="700" step="5" value="300">
          </div>'''
side = '''        <div class="block">
          <h3>Spherical mirror</h3>
          \\[ f = \\frac{R}{2}, \\qquad \\frac{1}{f} = \\frac{1}{s_1} + \\frac{1}{s_2} \\]
          <div class="ed-readout"><span>Radius <i>R</i></span><b id="mirrorRMetric">+160 mm</b></div>
          <div class="ed-readout"><span>Focal length <i>f</i></span><b id="mirrorFMetric">+80 mm</b></div>
          <div class="ed-readout"><span>Image distance <i>s</i>₂</span><b id="mirrorImageMetric">+109 mm</b></div>
          <div class="ed-readout"><span>Magnification <i>m</i></span><b id="mirrorMagMetric">−0.36</b></div>
          <p class="ed-text">A real object has \\(s_1 > 0\\). Concave mirrors have \\(f > 0\\), convex mirrors \\(f < 0\\). A real image has \\(s_2 > 0\\), a virtual image \\(s_2 < 0\\).</p>
        </div>
        <p id="mirrorStatus" class="ed-status" aria-live="polite">The current concave mirror forms a real, inverted image.</p>
        <span id="mirrorTypeBadge" hidden></span>
        <div class="ed-howto">
          <h3>Three principal rays</h3>
          <p>For a concave mirror: a ray parallel to the axis reflects through <i>F</i>; a ray through <i>F</i> reflects parallel; a ray through the centre of curvature <i>C</i> retraces its path. For a convex mirror the reflected rays diverge as if they came from the virtual <i>F</i> and <i>C</i> behind the mirror.</p>
        </div>'''
new = panel('mirror', 'Curved mirror ray diagram', 'Explore spherical concave and convex mirrors in the paraxial approximation.',
            plate, 'An object in front of a spherical mirror. The reflected principal rays locate the image; <i>F</i> is the focal point and <i>C</i> the centre of curvature.',
            None, '1fr 1.3fr 1.3fr', controls, side, caption_id='mirrorCaption')
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 5. Off-axis
i, j = grab('  <section id="panel-off-axis"')
plate = '''          <canvas id="offAxisCanvas" width="860" height="390" role="img" aria-label="Ray diagram showing a converging lens focusing collimated off-axis rays to different points on its back focal plane."></canvas>'''
controls = '''          <div>
            <h4>Incident bundle</h4>
            <label for="offAxisAngle"><span>Angle <i>θ</i> to the axis</span><b id="offAxisAngleValue">+3.0°</b></label>
            <input id="offAxisAngle" type="range" min="-6" max="6" step="0.1" value="3">
          </div>
          <div>
            <h4>Presets</h4>
            <div class="pz pz3">
              <button id="offAxisNegativeBtn">Negative</button>
              <button id="offAxisCenterBtn" class="primary">On axis</button>
              <button id="offAxisPositiveBtn">Positive</button>
            </div>
          </div>'''
side = '''        <div class="block">
          <h3>Focal-plane image height</h3>
          \\[ y' = f \\tan\\theta \\approx f\\theta \\]
          <div class="ed-readout"><span>Bundle angle <i>θ</i></span><b id="offAxisAngleMetric">+3.0°</b></div>
          <div class="ed-readout"><span>Focal length <i>f</i></span><b id="offAxisFocalMetric">40 mm</b></div>
          <div class="ed-readout"><span>Image displacement <i>y′</i></span><b id="offAxisImageMetric">+2.1 mm</b></div>
          <div class="ed-readout"><span>Focal-plane error</span><b id="offAxisPlaneMetric">0.00 mm</b></div>
        </div>
        <p id="offAxisStatus" class="ed-status" aria-live="polite">At θ = +3.0°, the collimated bundle focuses on the back focal plane at y′ = +2.1 mm from the on-axis focal point F′.</p>
        <span id="offAxisStatusBadge" hidden></span>
        <div class="ed-howto">
          <h3>What to look for</h3>
          <p>The incoming rays are parallel to each other, but the whole bundle is tilted by <i>θ</i> with respect to the optical axis. Whatever the tilt, the lens brings the bundle to a point on the same back focal plane; only the height of that point changes.</p>
        </div>'''
new = panel('off-axis', 'Focusing collimated off-axis rays',
            'A collimated bundle at any angle still focuses on the lens\'s back focal plane. Changing the angle changes only the displacement from the on-axis focal point.',
            plate, 'A parallel bundle tilted by <i>θ</i> converges to a point on the back focal plane, a height <i>y′</i> above or below the axis.',
            None, '1.4fr 1fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 6. Eye focus
i, j = grab('  <section id="panel-eye-focus"')
plate = '''          <canvas id="eyeFocusCanvas" width="860" height="390" role="img" aria-label="Ray diagram showing an object in the front focal plane of a lens, both focal points of the first lens and eye lens, parallel rays between the lenses, and an inverted image tree that remains focused on the moving retina."></canvas>'''
controls = '''          <div>
            <h4>Eye position</h4>
            <label for="eyeFocusPosition"><span>Distance from first lens <i>d</i></span><b id="eyeFocusPositionValue">85 mm</b></label>
            <input id="eyeFocusPosition" type="range" min="55" max="115" step="1" value="85">
          </div>
          <div>
            <h4>Fixed</h4>
            <div class="ed-fixed">First lens \\(f = 40\\ \\mathrm{mm}\\); eye lens \\(f_{\\rm eye} = 17\\ \\mathrm{mm}\\). Eye lens and retina move together.</div>
          </div>'''
side = '''        <div class="block">
          <h3>Object at the focal plane</h3>
          <div class="ed-readout"><span>Object distance</span><b id="eyeFocusObjectMetric">40 mm = f</b></div>
          <div class="ed-readout"><span>Rays after first lens</span><b id="eyeFocusVergenceMetric">Parallel</b></div>
          <div class="ed-readout"><span>Eye-lens position <i>d</i></span><b id="eyeFocusPositionMetric">85 mm</b></div>
          <div class="ed-readout"><span>Retina focus error</span><b id="eyeFocusErrorMetric">0.00 mm</b></div>
          <p class="ed-text">Ideal thin-lens model: the object lies at \\(F_1\\) of the first lens, while the retina lies at \\(F'_{\\rm eye}\\), 17 mm behind the eye lens.</p>
        </div>
        <p id="eyeFocusStatus" class="ed-status" aria-live="polite">The eye is 85 mm behind the first lens. The incoming rays are still parallel, so the ideal eye focuses them exactly on the retina.</p>
        <span id="eyeFocusStatusBadge" hidden></span>
        <div class="ed-howto">
          <h3>What to look for</h3>
          <p>The rays leave the first lens parallel to each other. Sliding the eye changes where they hit the eye lens, not their angle, so the eye always focuses them to the same point on its back focal plane: the retina. A real finite aperture would eventually cause vignetting if the eye moved outside the beam.</p>
        </div>'''
new = panel('eye-focus', 'Eye motion with an object at the focal plane',
            'Move the eye axially. The object stays at the front focal plane of the first lens, so the rays reaching the eye remain parallel and the image stays on the retina.',
            plate, 'An object at the front focal plane of a lens sends parallel rays to a moving eye; the eye lens focuses them onto its retina wherever it sits.',
            None, '1.2fr 1.6fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 7. Microscope
i, j = grab('  <section id="panel-microscope"')
plate = '''          <canvas id="microscopeCanvas" width="860" height="390" role="img" aria-label="Compound microscope ray diagram with object plane, objective lens, intermediate image plane, eyepiece focal plane, eyepiece, human eye lens and retina."></canvas>'''
controls = '''          <div>
            <h4>Object position</h4>
            <label for="microObjectDistance"><span>Distance from objective <i>s</i><sub>obj</sub></span><b id="microObjectDistanceValue">23.6 mm</b></label>
            <input id="microObjectDistance" type="range" min="21.0" max="38.0" step="0.1" value="23.6">
          </div>
          <div>
            <h4>Focus</h4>
            <div class="ed-fixed">Correct distance: <b id="microCorrectValue">23.6 mm</b></div>
            <div class="pz pz1"><button id="microFocusBtn">Set correct focus</button></div>
          </div>'''
side = '''        <div class="block">
          <h3>Compound microscope</h3>
          <div class="ed-readout"><span>Objective</span><b id="microObjMetric">10× (f = 20 mm)</b></div>
          <div class="ed-readout"><span>Eyepiece</span><b id="microEyeMetric">5× (f = 50 mm)</b></div>
          <div class="ed-readout"><span>Intermediate image − eyepiece focal plane</span><b id="microOffsetMetric">0.0 mm</b></div>
          <div class="ed-readout"><span>Retina focus error</span><b id="microRetinaMetric">0.0 mm</b></div>
          <p class="ed-text">Dotted lines mark the principal planes; purple dots mark the focal points.</p>
        </div>
        <span id="microscopeStatusBadge" hidden></span>
        <div class="ed-howto">
          <h3>What to look for</h3>
          <p>When the object is at the correct distance, the intermediate image lands on the focal plane of the eyepiece. The eyepiece then sends out nearly parallel rays, and the fixed human-eye lens focuses them onto the retina.</p>
          <p>Move the object away from its correct distance and the retina is no longer sharply focused, even though the objective, eyepiece and eye lens stay fixed.</p>
        </div>'''
new = panel('microscope', 'Microscope with a human eye',
            'Move the object to explore focus. The objective forms an intermediate image, which the eyepiece magnifies and the eye focuses onto the retina.',
            plate, 'A compound microscope: objective, intermediate image, eyepiece, then the eye lens and retina.',
            None, '1.4fr 1fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 8. Telescope
i, j = grab('  <section id="panel-telescope"')
plate = '''          <canvas id="telescopeCanvas" width="860" height="390" role="img" aria-label="Keplerian telescope ray diagram with objective, intermediate image, eyepiece, human eye lens and retina."></canvas>'''
controls = '''          <div>
            <h4>Eyepiece position</h4>
            <label for="telescopeSeparation"><span>Objective–eyepiece separation <i>L</i></span><b id="telescopeSeparationValue">144.0 mm</b></label>
            <input id="telescopeSeparation" type="range" min="132" max="156" step="0.1" value="144.0">
          </div>
          <div>
            <h4>Focus</h4>
            <div class="ed-fixed">Normal adjustment: <b id="telescopeCorrectValue">144.0 mm</b></div>
            <div class="pz pz1"><button id="telescopeFocusBtn">Set normal adjustment</button></div>
          </div>'''
side = '''        <div class="block">
          <h3>Keplerian telescope</h3>
          \\[ L = f_{\\rm obj} + f_{\\rm eye}, \\qquad M = -\\frac{f_{\\rm obj}}{f_{\\rm eye}} \\]
          <div class="ed-readout"><span>Objective <i>f</i><sub>obj</sub></span><b id="telObjMetric">120 mm</b></div>
          <div class="ed-readout"><span>Eyepiece <i>f</i><sub>eye</sub></span><b id="telEyeMetric">24 mm</b></div>
          <div class="ed-readout"><span>Separation <i>L</i></span><b id="telSepMetric">144.0 mm</b></div>
          <div class="ed-readout"><span>Angular magnification <i>M</i></span><b id="telMagMetric">−5.0×</b></div>
          <p class="ed-text">Purple dots mark focal points; the negative sign denotes an inverted view.</p>
        </div>
        <span id="telescopeStatusBadge" hidden></span>
        <div class="ed-howto">
          <h3>What to look for</h3>
          <p>At normal adjustment the real intermediate image formed by the objective lies at the front focal plane of the eyepiece, so the rays leaving the eyepiece are parallel.</p>
          <p>Move the eyepiece away from this position and the outgoing rays converge or diverge, so the fixed eye lens no longer forms a sharp image exactly on the retina.</p>
        </div>'''
new = panel('telescope', 'Keplerian telescope with a human eye',
            'At normal adjustment, the objective and eyepiece produce parallel rays that the eye focuses onto the retina.',
            plate, 'A distant object sends parallel rays into the objective; the eyepiece re-collimates them for the eye.',
            None, '1.4fr 1fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ 9. Aberrations
i, j = grab('  <section id="panel-aberrations"')
plate = '''          <canvas id="aberrCanvas" width="860" height="390" role="img" aria-label="Interactive lens aberration ray diagram."></canvas>'''
controls = '''          <div>
            <h4>Aberration</h4>
            <div class="pz pz3 aberr-button-grid">
              <button id="aberrSphericalBtn" class="primary">Spherical</button>
              <button id="aberrChromaticBtn">Chromatic</button>
              <button id="aberrComaBtn">Coma</button>
              <button id="aberrAstigBtn">Astigmatism</button>
              <button id="aberrDistortionBtn">Distortion</button>
            </div>
          </div>
          <div>
            <h4>Lens model</h4>
            <div class="pz aberr-button-grid">
              <button id="aberrRealBtn" class="primary">Real lens</button>
              <button id="aberrIdealBtn">Ideal thin lens</button>
            </div>
          </div>
          <div>
            <h4>Parameters</h4>
            <div id="aberrSphericalControls" class="aberr-control-group">
              <label for="aberrAperture"><span>Aperture <i>D</i></span><b id="aberrApertureValue">60 mm</b></label>
              <input id="aberrAperture" type="range" min="20" max="100" step="1" value="60">
            </div>
            <div id="aberrChromaticControls" class="aberr-control-group" hidden>
              <div class="pz aberr-button-grid">
                <button id="aberrWhiteBtn" class="primary">White light</button>
                <button id="aberrMonoBtn">Single <i>λ</i></button>
              </div>
              <div id="aberrWavelengthWrap" hidden>
                <label for="aberrWavelength"><span>Wavelength <i>λ</i></span><b id="aberrWavelengthValue">550 nm</b></label>
                <input id="aberrWavelength" type="range" min="450" max="650" step="1" value="550">
              </div>
            </div>
            <div id="aberrComaControls" class="aberr-control-group" hidden>
              <label for="aberrComaField"><span>Field angle <i>θ</i></span><b id="aberrComaFieldValue">3.0°</b></label>
              <input id="aberrComaField" type="range" min="0.0" max="6.0" step="0.1" value="3.0">
            </div>
            <div id="aberrAstigControls" class="aberr-control-group" hidden>
              <label for="aberrAstigField"><span>Field angle <i>θ</i></span><b id="aberrAstigFieldValue">3.0°</b></label>
              <input id="aberrAstigField" type="range" min="0.0" max="6.0" step="0.1" value="3.0">
              <label for="aberrAstigScreen"><span>Screen position <i>T</i> → <i>S</i></span><b id="aberrAstigScreenValue">50%</b></label>
              <input id="aberrAstigScreen" type="range" min="0" max="100" step="1" value="50">
            </div>
            <div id="aberrDistortionControls" class="aberr-control-group" hidden>
              <label for="aberrDistField"><span>Field angle <i>θ</i></span><b id="aberrDistFieldValue">4.5°</b></label>
              <input id="aberrDistField" type="range" min="0.0" max="6.0" step="0.1" value="4.5">
              <label for="aberrDistStrength"><span>Strength</span><b id="aberrDistStrengthValue">+35%</b></label>
              <input id="aberrDistStrength" type="range" min="-45" max="45" step="1" value="35">
              <div class="ed-fixed">Negative: barrel. Positive: pincushion.</div>
            </div>
          </div>'''
side = '''        <div class="block">
          <h3 id="aberrStatusBadge">Spherical aberration</h3>
          <div class="ed-readout"><span id="aberrMetric1Label">Aperture <i>D</i></span><b id="aberrMetric1">60 mm</b></div>
          <div class="ed-readout"><span id="aberrMetric2Label">Paraxial focus</span><b id="aberrMetric2">80.0 mm</b></div>
          <div class="ed-readout"><span id="aberrMetric3Label">Marginal focus</span><b id="aberrMetric3">74.8 mm</b></div>
          <div class="ed-readout"><span id="aberrMetric4Label">Longitudinal Δ<i>f</i></span><b id="aberrMetric4">5.2 mm</b></div>
          <p id="aberrMetricNote" class="ed-text">Closing the aperture removes marginal rays, so the paraxial approximation becomes better.</p>
        </div>
        <div class="ed-howto">
          <h3>What to look for</h3>
          <p id="aberrExplanation">Marginal rays focus closer to the lens than paraxial rays. Reduce the aperture and the two focal positions approach one another.</p>
          <p class="ed-text">Chromatic model: shorter wavelengths see a larger refractive index and therefore a shorter focal length.</p>
        </div>'''
new = panel('aberrations', 'Lens aberrations',
            'Compare the ideal paraxial lens with simple models of spherical aberration, chromatic aberration, coma, astigmatism and distortion.',
            plate, 'Rays through a real lens, compared with the ideal thin-lens focus.',
            None, '1.5fr 1fr 1.4fr', controls, side)
s = s[:i] + new + s[j:]

# ------------------------------------------------------------------ CSS additions for the template pieces used above
rep("  .ed-status{line-height:1.6;border-left:3px solid var(--accent);padding-left:12px;margin:0}",
    """  .ed-status{line-height:1.6;border-left:3px solid var(--accent);padding-left:12px;margin:0}
  .ed-text{font-size:14.5px;color:var(--muted);line-height:1.55;margin:8px 0 0}
  .ed-fixed{font-size:14px;color:var(--muted);line-height:1.5;margin-top:6px}
  .ed-fixed b{font-weight:500;color:var(--text)}
  .ed-controls .pz.pz3{grid-template-columns:1fr 1fr 1fr}
  .ed-controls .pz.pz1{grid-template-columns:1fr}
  .ed-controls .pz button.primary{background:var(--text);color:#fff;border-color:var(--text)}
  .ed-controls .refraction-presets #tirBtn{grid-column:1 / -1}
  .ed-controls .aberr-button-grid button.primary{background:var(--text);color:#fff;border-color:var(--text)}
  .ed-side .ed-readout + .ed-readout{border-top:1px dotted var(--border)}
  .ed-side .ed-readout span{font-size:14.5px}
  .ed-plate .ed-two{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:0;background:#fff;border:0}
  .ed-plate .ed-two > div{background:#fff;border:0}
  .ed-plate .ed-two > div + div{border-left:1px solid var(--border)}
  .ed-panel-h{font:500 15px var(--serif);color:var(--text);padding:6px 10px;border-bottom:1px solid var(--border)}
  .ed-plate .wave-left-panel svg,.ed-plate #waveCanvas{height:360px}
  .ed-plate #raySvg{height:420px;background:#fff}
  .ed-plate canvas:not(#lensCanvas){width:100%;height:auto}
  @media (max-height:800px){
    .ed-plate canvas:not(#lensCanvas){width:auto;height:auto;max-width:100%;max-height:300px;margin:0 auto}
    .ed-plate .wave-left-panel svg,.ed-plate #waveCanvas{height:280px}
    .ed-plate #raySvg{height:320px}
  }""")

# the wave tab's old wrapper styles must not fight the plate
rep("  .ed-plate{background:#fff;border:1px solid var(--border);padding:8px}","  .ed-plate{background:#fff;border:1px solid var(--border);padding:8px}\n  .ed-plate .wave-visuals{margin:0}\n  .ed-plate .wave-canvas-wrap{padding:0;border:0}")

# ------------------------------------------------------------------ JS: badge writes now target hidden spans or the aberration heading (fine); remove dead refs
for idm in ['mirrorTypeBadge', 'offAxisStatusBadge', 'eyeFocusStatusBadge', 'microscopeStatusBadge', 'telescopeStatusBadge', 'aberrStatusBadge']:
    assert f'id="{idm}"' in s, idm

open(p, 'w').write(s)
print('ok')
