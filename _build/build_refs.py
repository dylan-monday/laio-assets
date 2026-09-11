#!/usr/bin/env python3
"""Render the Range references to PNG.

    python3 _build/build_refs.py

Each ai/laio-brand/references/NN-name.html is rendered to NN-name.png next to
it, at 1600x900, in headless Chrome. The HTML is what an AI reads. The PNG is
what Claude Design and people see. Rerun after editing any reference, then
rerun gen_pages.py and rezip the skill.

Needs Google Chrome or Chromium. Set CHROME to its path if it is not found.
"""
import glob, os, pathlib, shutil, subprocess, tempfile, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(REPO, "ai", "laio-brand", "references")

CANDIDATES = [
    os.environ.get("CHROME"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
]
chrome = next((c for c in CANDIDATES if c and os.path.exists(c)), None)
if not chrome:
    raise SystemExit("build_refs: Chrome not found. Set CHROME to the browser binary.")

pages = sorted(glob.glob(os.path.join(REFS, "*.html")))
if not pages:
    raise SystemExit(f"build_refs: no references in {REFS}")

def render(page, png):
    """Render one page to PNG. On macOS, headless Chrome writes the file and then
    does not always exit, so wait for the PNG to stop growing and close it."""
    if os.path.exists(png):
        os.remove(png)
    # A fresh profile per page, so nothing cached carries between renders.
    # The virtual time budget lets the embedded fonts load before the capture.
    with tempfile.TemporaryDirectory() as profile:
        proc = subprocess.Popen([
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=1600,900",
            "--virtual-time-budget=5000", "--allow-file-access-from-files",
            f"--user-data-dir={profile}", f"--screenshot={png}",
            pathlib.Path(page).as_uri(),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        size, deadline = -1, time.time() + 60
        while time.time() < deadline:
            time.sleep(0.5)
            if os.path.exists(png) and os.path.getsize(png) > 0:
                if os.path.getsize(png) == size:
                    break
                size = os.path.getsize(png)
            elif proc.poll() is not None:
                break
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    if not os.path.exists(png):
        raise SystemExit(f"build_refs: no screenshot for {os.path.relpath(page, REPO)}")

for page in pages:
    png = page[:-5] + ".png"
    render(page, png)
    print(os.path.relpath(png, REPO), os.path.getsize(png), "bytes")
