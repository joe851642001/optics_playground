# Optics Playground: GitHub Pages + Plausible setup

This site is designed to be hosted as a static GitHub Pages website, while usage statistics live separately in Plausible Analytics.

## What the site tracks after Plausible is enabled

Plausible automatically records page views with timestamps and an approximate visitor country.

The webpage also sends a small number of custom events:

- `Tab Opened - Wave to Ray`
- `Tab Opened - Refraction`
- `Tab Opened - Interference`
- `Tab Opened - Diffraction`
- `Tab Opened - Polarisation`
- `Tab Opened - Quantum Optics`
- `Simulation Started - Wave to Ray`
- `Ray Limit Explored - Wave to Ray`
- `Simulation Started - Refraction`
- `TIR Reached - Refraction`
- `Critical Angle Reached - Refraction`
- `Preset - Air to Glass`
- `Preset - Water to Air`
- `Preset - Glass to Air`
- `Preset - Diamond to Air`

The code deliberately does **not** send every slider movement.

No name, email address, student ID or questionnaire response is collected by this webpage.

## 1. Publish on GitHub Pages

1. Sign in to GitHub.
2. Create a new repository. A name such as `optics-playground` works well.
3. Upload these files to the repository root:
   - `index.html`
   - `.nojekyll`
   - `README.md` (optional)
   - `SETUP.md` (optional)
4. Open **Settings** for the repository.
5. Open **Pages** in the left sidebar.
6. Under **Build and deployment**, choose **Deploy from a branch**.
7. Select branch **main** and folder **/(root)**.
8. Click **Save**.
9. GitHub will give you a public URL, usually similar to:
   `https://YOUR-USERNAME.github.io/optics-playground/`

## 2. Create the Plausible site

1. Create/sign in to a Plausible Analytics account.
2. Add a website.
3. For a GitHub Pages project URL such as:
   `https://YOUR-USERNAME.github.io/optics-playground/`
   use the hostname:
   `YOUR-USERNAME.github.io`
4. Set the reporting timezone you want.
5. Open the site's installation/tracking settings.
6. Copy the complete site-specific tracking snippet Plausible gives you.

## 3. Paste the Plausible snippet into index.html

Near the top of `index.html`, inside `<head>`, there is a large comment beginning:

`PLAUSIBLE ANALYTICS SETUP`

Paste the complete Plausible site-specific snippet immediately below that comment.

Do not invent the script URL and do not use the example `pa-XXXXX.js` URL. Plausible gives every site its own current snippet.

Then commit/upload the updated `index.html` to GitHub.

## 4. Verify analytics

1. Open the published GitHub Pages site in a browser.
2. Move a slider in Refraction.
3. Try the **Try TIR!** button.
4. Return to Plausible and use its site-installation verification.
5. Once events start arriving, add the event names above as custom-event goals if you want them highlighted as conversions/goals.

## 5. Viewing statistics by year and country

You do not need to ask visitors which year they are in.

Every visit/event has a date. In Plausible, choose a date range such as:
- 1 Jan 2026 to 31 Dec 2026
- 1 Jan 2027 to 31 Dec 2027

Use the Countries report/filter for approximate visitor country.

This means you can compare 2026, 2027, 2028, etc. without changing the webpage.

## 6. Adding more tabs later

The webpage already has placeholder tabs for:
- Interference
- Diffraction
- Polarisation
- Quantum Optics

You can replace each placeholder panel with a real activity later.

Historical analytics are **not stored in the HTML or GitHub repository**. They remain in the Plausible site/dashboard as long as you keep using the same Plausible site/account and do not delete that analytics data.

Updating `index.html`, adding tabs or redesigning the site does not erase previous analytics.

For long-term consistency, keep old event names stable. If an event is renamed, the old event history remains but the new name will appear as a separate event series.
