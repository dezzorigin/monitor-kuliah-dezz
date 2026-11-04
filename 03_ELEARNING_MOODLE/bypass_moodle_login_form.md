# Penjelasan Teknis: Penanganan Form Login Ganda Moodle USK

## Masalah:
Pada Moodle USK (`https://elearning.usk.ac.id/login/index.php`), terdapat dua elemen `<form>`:
- Form 1 (`#login`): Input username dan password mahasiswa/dosen.
- Form 2 (`#guestlogin`): Tombol "Login as a guest".

Library otomasi browser standar seperti ekstensi autofill atau `browser_vault_fill` sering gagal karena mendeteksi form ganda dan tidak dapat memutuskan input mana yang harus diisi.

## Solusi:
Gunakan evaluasi JavaScript langsung pada konteks browser dengan memanggil **Property Descriptor Setter** bawaan HTMLInputElement prototype:
```javascript
const setVal = (el, val) => {
    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    setter.call(el, val);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
};

setVal(document.querySelector('#username'), '250810701100090');
setVal(document.querySelector('#password'), sandi_rahasia);
document.querySelector('#login button[type="submit"]').click();
```
Dispatcing event `input` dan `change` wajib dilakukan agar state framework Moodle (YUI / AMD / jQuery) menyadari bahwa input telah terisi sebelum tombol submit diklik.
