# Panduan Solver CAPTCHA SIMKULIAH (ddddocr)

## Mengapa ddddocr?
- Model Vision LLM sering menolak membaca teks CAPTCHA karena alasan kebijakan filter privasi atau framing bot.
- Tesseract OCR konvensional memiliki akurasi rendah (< 40%) pada font bergelombang dan noise garis SIMKULIAH.
- `ddddocr` (Deep Learning-based OCR untuk Python) memiliki akurasi **> 98%** pada CAPTCHA SIMKULIAH dan KRS USK dengan waktu inferensi lokal hanya **~30 milidetik** tanpa memerlukan koneksi internet.

## Cara Instalasi:
```bash
uv venv .venv-captcha
uv pip install --python .venv-captcha/bin/python ddddocr pillow requests
```

## Implementasi Python Sederhana:
```python
import ddddocr
import requests
import time

ocr = ddddocr.DdddOcr(show_ad=False)
sess = requests.Session()

# 1. Ambil halaman login untuk mengikat ci_session
sess.get("https://simkuliah.usk.ac.id/")

# 2. Ambil gambar captcha dengan timestamp unik
cap_res = sess.get(f"https://simkuliah.usk.ac.id/index.php/login/captcha_image?t={int(time.time())}")

# 3. Klasifikasi OCR langsung dari byte memory
captcha_text = ocr.classification(cap_res.content)
print(f"Hasil CAPTCHA: {captcha_text}")
```
