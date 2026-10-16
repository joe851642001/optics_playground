# GitHub Pages + Google Analytics 4

This site is already configured with GA4 measurement ID:

`G-VB4PLZGGJV`

## Publish on GitHub Pages
1. Upload `index.html`, `.nojekyll`, `README.md`, `SETUP.md` and `OPTICS_PLAYGROUND_HANDOFF.md` to the root of your GitHub repository (the site needs only `index.html` and `.nojekyll`; KaTeX and the fonts load from CDNs).
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose **main** and **/(root)**.
5. Save.

## Check Analytics
After the site is live:
1. Open Google Analytics.
2. Go to **Reports → Realtime**.
3. Open your GitHub Pages site in another tab.
4. Click different tabs and use the simulations.
5. Look for page views and custom events.

## Custom events (as embedded on 16 October 2026)
All events are sent through one helper, `track(eventName, params)`, which calls `gtag('event', …)` only if GA has loaded. No slider movements are sent, and no student-identifying data is collected.

| Event | Parameters | When it fires |
|---|---|---|
| `tab_opened` | `activity` = tab name (`wave-ray`, `fermat`, `refraction`, `lens`, `mirror`, `off-axis`, `eye-focus`, `microscope`, `telescope`, `aberrations`) | first time a tab is opened in a session |
| `simulation_started` | `activity` ∈ `wave_to_ray`, `fermat`, `refraction`, `lens`, `mirror`, `off_axis_focus`, `eye_focus`, `microscope`, `telescope`, `aberrations` | first interaction with that activity's controls |
| `ray_limit_explored` | `activity = wave_to_ray` | the diffraction width drops below the screen resolution |
| `tir_reached` | `activity = refraction` | total internal reflection is reached |
| `critical_angle_reached` | `activity = refraction` | the incident angle reaches the critical angle |
| `preset_used` | `activity` + `preset`: refraction `air_to_glass` / `water_to_air` / `glass_to_air`; off-axis `on_axis` / `positive_angle` / `negative_angle`; telescope `normal_adjustment` / `keplerian` / `galilean`; aberrations `spherical` / `chromatic` / `coma` / `astigmatism` / `distortion` / `real_lens` / `ideal_lens` | a preset or mode button is pressed |

GA4 timestamps events automatically, so you can compare 2026, 2027, etc. by changing the report date range. Country is also available as a geographic dimension.

Historical analytics are stored in Google Analytics, not in the HTML file. Updating the site or adding future tabs will not erase old analytics as long as you keep the same GA4 property / measurement ID.

Privacy note: review the University of Bath's current cookie/privacy requirements before broad public deployment of Google Analytics.
