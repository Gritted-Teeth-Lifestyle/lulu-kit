---
name: iphonetest
description: Open any URL in an iPhone 14 Pro viewport for mobile layout testing
---

# iPhone Test

Test any web page in an iPhone 14 Pro viewport using Playwright. Takes a screenshot and saves it to `screen.png` for visual inspection.

## WHEN_TO_USE

Use this skill when you need to:
- Check how a web page looks on mobile
- Debug responsive layout issues
- Verify mobile-specific UI behavior or interactions
- Test touch targets, font sizes, overflow, and viewport rendering

## HOW_TO_USE

The tool is at: `<HOME>\.claude\skills\iphonetest\iphonetest.py`

### Basic screenshot
```powershell
python <HOME>\.claude\skills\iphonetest\iphonetest.py https://example.com
```
- Opens the URL in iPhone 14 Pro viewport (390×844, device scale 3×, mobile UA)
- Waits for `networkidle` + 1.5s extra render time
- Saves screenshot to `<HOME>\claude-vision\screen.png`

### Custom output path
```powershell
python <HOME>\.claude\skills\iphonetest\iphonetest.py https://example.com --output C:\path\to\output.png
```

### Read the result
```python
Read("<HOME>/claude-vision/screen.png")
```

## DEVICE SPECS

| Property | Value |
|---|---|
| Viewport | 390 × 844 |
| Device scale | 3× |
| User agent | iPhone iOS 17 / Safari |
| Touch | enabled |
| Mobile | true |

## RULES

- Always read the screenshot after capturing — report what you see, not what you expect
- If the page looks broken, check for JS errors or slow-loading resources
- Use `--output` when testing multiple URLs to avoid overwriting results
