#!/usr/bin/env python3
"""krs_login.py — full-Python login KRS USK (Laravel) + bypass captcha.

Beda dengan SIMKULIAH (CodeIgniter):
  - CSRF token: hidden input `_token` di form -> wajib di-scrape tiap GET /auth
  - Field: nim / password / captcha
  - Captcha: GET /auth/captcha (session-bound via laravel_session cookie)

ddddocr di-import malas (lazy) supaya modul bisa di-import tanpa OCR
terpasang (mis. untuk inspeksi / tests yang tidak butuh login).
"""
import os
import re
import sys
import time

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://krs.usk.ac.id"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

_OCR = None


def get_ocr():
    global _OCR
    if _OCR is None:
        import ddddocr
        _OCR = ddddocr.DdddOcr(show_ad=False)
    return _OCR


def _default_workdir():
    data_dir = os.environ.get("MONITOR_KULIAH_DATA_DIR",
                              "/opt/data/monitor-kuliah")
    return os.path.join(data_dir, "tmp")


def fetch_login(sess):
    r = sess.get(BASE + "/auth", headers={"User-Agent": UA}, verify=False, timeout=20)
    r.raise_for_status()
    m = re.search(r'name="_token" value="([^"]+)"', r.text)
    return r.text, (m.group(1) if m else None)


def solve_captcha(sess, save_path=None):
    r = sess.get(f"{BASE}/auth/captcha?t={int(time.time()*1000)}",
                 headers={"User-Agent": UA, "Referer": BASE + "/auth"},
                 verify=False, timeout=20)
    r.raise_for_status()
    if save_path:
        open(save_path, "wb").write(r.content)
    return get_ocr().classification(r.content)


def post_login(sess, nim, password, token, captcha):
    r = sess.post(BASE + "/auth",
                  data={"_token": token, "nim": nim, "password": password,
                        "captcha": captcha},
                  headers={"User-Agent": UA, "Referer": BASE + "/auth"},
                  verify=False, timeout=20, allow_redirects=True)
    body = r.text.lower()
    if "/auth" in r.url and "dashboard" not in r.url.lower():
        return r, "gagal"
    return r, "ok"


def login(nim, password, max_retry=6, workdir=None):
    workdir = workdir or _default_workdir()
    os.makedirs(workdir, exist_ok=True)
    sess = requests.Session()
    log = []
    for attempt in range(1, max_retry + 1):
        html, token = fetch_login(sess)
        save = f"{workdir}/krs_cap_{int(time.time())}_{attempt}.png"
        jawaban = solve_captcha(sess, save_path=save)
        jawaban = re.sub(r"[^A-Za-z0-9]", "", jawaban)[:5]
        log.append(f"try{attempt}: ocr='{jawaban}' file={save}")
        r, verdict = post_login(sess, nim, password, token, jawaban)
        log.append(f"  -> {verdict} @ {r.url}")
        if verdict == "ok":
            return sess, log
    return None, log


if __name__ == "__main__":
    import getpass
    nim = sys.argv[1] if len(sys.argv) > 1 else input("NIM: ")
    pw = sys.argv[2] if len(sys.argv) > 2 else getpass.getpass("Password: ")
    sess, log = login(nim, pw)
    print("\n".join(log))
    print("LOGIN OK" if sess else "LOGIN GAGAL")
