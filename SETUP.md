# GitHub Pages + Google Analytics 4

This site is already configured with GA4 measurement ID:

`G-VB4PLZGGJV`

## Publish on GitHub Pages
1. Upload `index.html`, `.nojekyll`, `README.md`, and `SETUP.md` to the root of your GitHub repository.
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

## Custom events
- `tab_opened` with parameter `activity`
- `simulation_started` with parameter `activity`
- `ray_limit_explored` with `activity = wave_to_ray`
- `tir_reached` with `activity = refraction`
- `critical_angle_reached` with `activity = refraction`
- `preset_used` with parameters `activity` and `preset`

GA4 timestamps events automatically, so you can compare 2026, 2027, etc. by changing the report date range. Country is also available as a geographic dimension.

Historical analytics are stored in Google Analytics, not in the HTML file. Updating the site or adding future tabs will not erase old analytics as long as you keep the same GA4 property / measurement ID.

Privacy note: review the University of Bath's current cookie/privacy requirements before broad public deployment of Google Analytics.
