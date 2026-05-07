#!/usr/bin/env python3
"""
iphonetest.py — Open a URL in iPhone 14 Pro viewport and screenshot it.
Usage: python iphonetest.py <url> [--output path/to/output.png]
"""
import sys, argparse, os
from playwright.sync_api import sync_playwright

IPHONE = {
    "viewport": {"width": 390, "height": 844},
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--output", default=os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "claude-vision", "screen.png"))
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(**IPHONE)
        page = ctx.new_page()
        page.goto(args.url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1500)
        page.screenshot(path=args.output, full_page=False)
        browser.close()

    print(f"Screenshot saved to {args.output}")

if __name__ == "__main__":
    main()
