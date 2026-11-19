#!/usr/bin/env python3
"""Gate statis landing monitor-kuliah-dezz — jalan di CI (job static-checks).
1. Larangan P0 anti-slop (lihat docs/DESIGN.md + ui-anti-slop.md).
2. Tag OG/Twitter lengkap + URL absolut ke og-image.png.
3. Data asli repo: 13 MK, 21 SKS, entri log contoh dilabeli jujur.
4. styles.css tanpa gradient; app.js tanpa data placeholder.
Usage: python3 scripts/check-static.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANDING = os.path.join(ROOT, "landing")

failures = []


def check(cond, msg):
    if cond:
        print("  ok: " + msg)
    else:
        failures.append(msg)
        print("  FAIL: " + msg)


def main():
    html = open(os.path.join(LANDING, "index.html"), encoding="utf-8").read()
    css = open(os.path.join(LANDING, "styles.css"), encoding="utf-8").read()
    js = open(os.path.join(LANDING, "app.js"), encoding="utf-8").read()

    print("P0 anti-slop:")
    check(not re.search(r"linear-gradient|radial-gradient|bg-clip-text",
                        html + css, re.I), "tanpa gradient / bg-clip-text")
    check(not re.search(r"font-family:\s*[\"']?(Inter|Roboto)", css, re.I),
          "tanpa Inter/Roboto sebagai font utama")
    check(not re.search(r"Elevate your workflow|Unlock the power|10x faster"
                        r"|99\.9% uptime", html, re.I),
          "tanpa copy generik / statistik vanity")
    emoji = re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", html)
    check(not emoji, "tanpa emoji mentah sebagai ikon"
          + (f" ({emoji.group(0)})" if emoji else ""))
    check("rounded-2xl" not in html, "tanpa rounded-2xl shadow-lg massal")
    check("lorem ipsum" not in html.lower(), "tanpa lorem ipsum")

    print("OG/Twitter:")
    for tag in [
        'property="og:title"',
        'property="og:description"',
        'property="og:type"',
        'property="og:url" content="https://monitor-kuliah-dezz.pages.dev/"',
        'property="og:image" content="https://monitor-kuliah-dezz.pages.dev/og-image.png"',
        'name="twitter:card" content="summary_large_image"',
        'name="twitter:title"',
        'name="twitter:description"',
        'name="twitter:image" content="https://monitor-kuliah-dezz.pages.dev/og-image.png"',
    ]:
        check(tag in html, "tag " + tag)

    print("Data asli repo:")
    lessons = len(re.findall(r'<tr class="mk-row"', html))
    check(lessons == 13, f"13 baris mata kuliah (dapat {lessons})")
    check("21 SKS" in html, "21 SKS disebut")
    check("Sabtu" in html and "bentrok" in html,
          "bentrok Sabtu 08.00 didokumentasikan")
    check("contoh" in html, "entri log contoh dilabeli contoh dengan jujur")
    check("SINF2023" in html and "250810701100090" in html,
          "data contoh dari template state repo (SINF2023, NPM)")
    entries = len(re.findall(r'<article class="log-entry"', html))
    check(entries >= 6, f"linimasa log >= 6 entri (dapat {entries})")

    print("CSS/JS:")
    check("linear-gradient" not in css, "styles.css tanpa gradient")
    check("prefers-reduced-motion" in css, "prefers-reduced-motion dihormati")
    check(":focus-visible" in css, "focus-visible ada")
    check("Asia/Jakarta" in js, "app.js pakai zona Asia/Jakarta")

    print("File deploy:")
    for f in ("index.html", "styles.css", "app.js", "favicon.svg", "og-image.png"):
        p = os.path.join(LANDING, f)
        check(os.path.isfile(p) and os.path.getsize(p) > 0, f"{f} ada & tidak kosong")
    og = os.path.join(LANDING, "og-image.png")
    if os.path.isfile(og):
        check(os.path.getsize(og) >= 10 * 1024,
              f"og-image.png >= 10KB (dapat {os.path.getsize(og)} byte)")

    if failures:
        print(f"\n{len(failures)} kegagalan gate statis")
        return 1
    print("\nOK: semua gate statis lolos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
