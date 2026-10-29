# agent/checks.py
from playwright.sync_api import sync_playwright

URL = "http://localhost:5173/"

# Runs inside the browser. Returns plain numbers and a list of offending elements.
OVERFLOW_JS = """
() => {
  const vw = document.documentElement.clientWidth;
  const sw = document.documentElement.scrollWidth;
  const offenders = [];
  for (const el of document.body.querySelectorAll("*")) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > vw + 1 || r.left < -1) {
      offenders.push({
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        cls: typeof el.className === "string" ? el.className : null,
        text: (el.textContent || "").trim().slice(0, 40),
        left: Math.round(r.left),
        right: Math.round(r.right),
      });
    }
  }
  return {
    viewport_width: vw,
    scroll_width: sw,
    overflow_px: sw - vw,
    offenders: offenders.slice(0, 10),
  };
}
"""


def check_horizontal_overflow(page):
    """Measure overflow on an already-loaded page. Returns a dict."""
    return page.evaluate(OVERFLOW_JS)


def assert_no_horizontal_overflow(result):
    """Raise AssertionError if the measurement shows overflow."""
    if result["overflow_px"] > 1 or result["offenders"]:
        raise AssertionError(
            f"Horizontal overflow: page is {result['overflow_px']}px wider "
            f"than the {result['viewport_width']}px viewport, "
            f"{len(result['offenders'])} element(s) stick out."
        )


if __name__ == "__main__":
    # Standalone run: check the healthy page on a Pixel 7.
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(**p.devices["Pixel 7"])
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")

        result = check_horizontal_overflow(page)
        print(result)

        try:
            assert_no_horizontal_overflow(result)
            print("PASS: no horizontal overflow")
        except AssertionError as e:
            print(f"FAIL: {e}")

        ctx.close()
        browser.close()