# agent/capture.py
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://localhost:5173/"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "screenshots"


def capture():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop: a plain browser window of 1440x900 CSS pixels
        desktop_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = desktop_ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        desktop_path = OUTPUT_DIR / "desktop.png"
        page.screenshot(path=str(desktop_path), full_page=True)
        print(f"Saved {desktop_path}")
        desktop_ctx.close()

        # Mobile: emulate a Pixel 7 (small viewport, touch, mobile user agent)
        mobile_ctx = browser.new_context(**p.devices["Pixel 7"])
        page = mobile_ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        mobile_path = OUTPUT_DIR / "mobile.png"
        page.screenshot(path=str(mobile_path), full_page=True)
        print(f"Saved {mobile_path}")
        mobile_ctx.close()

        browser.close()


if __name__ == "__main__":
    capture()