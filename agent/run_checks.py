# agent/run_checks.py
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from checks import check_horizontal_overflow, assert_no_horizontal_overflow
from defects import DEFECTS

URL = "http://localhost:5173/"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "screenshots"


def run_scenario(p, browser, name, css):
    """Load the page on a Pixel 7, optionally inject a defect, measure, screenshot."""
    ctx = browser.new_context(**p.devices["Pixel 7"])
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")

    if css:
        page.add_style_tag(content=css)  # inject the defect at runtime

    result = check_horizontal_overflow(page)

    shot = OUTPUT_DIR / f"mobile_{name}.png"
    page.screenshot(path=str(shot), full_page=True)
    ctx.close()

    try:
        assert_no_horizontal_overflow(result)
        return result, True, "", shot
    except AssertionError as e:
        return result, False, str(e), shot


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # (name, css, should_the_check_pass)
    scenarios = [("healthy", None, True)]
    scenarios += [(name, css, False) for name, css in DEFECTS.items()]

    all_ok = True
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, css, expected_pass in scenarios:
            result, passed, message, shot = run_scenario(p, browser, name, css)

            print(f"\n=== {name} ===")
            print(f"viewport={result['viewport_width']}px  "
                  f"scroll={result['scroll_width']}px  "
                  f"overflow={result['overflow_px']}px")
            for o in result["offenders"]:
                print(f"  offender: <{o['tag']}> class={o['cls']!r} "
                      f"left={o['left']} right={o['right']}")
            print("check:", "PASS" if passed else f"FAIL - {message}")
            print("screenshot:", shot)

            if passed == expected_pass:
                print("verdict: as expected" if passed else "verdict: DEFECT DETECTED")
            else:
                print("verdict: UNEXPECTED RESULT")
                all_ok = False

        browser.close()

    print("\nSUMMARY:", "all scenarios behaved as expected" if all_ok else "problems found")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()