/* Monitor Kuliah Dezz — interaksi landing (tanpa dependensi).
   Zona waktu: Asia/Jakarta. Tidak ada data placeholder: filter hanya
   menyaring entri contoh yang memang ada di halaman. */
(function () {
  "use strict";

  /* ——— tanggal hari ini (Asia/Jakarta) ——— */
  var HARI = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
  var BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
               "Jul", "Agu", "Sep", "Okt", "Nov", "Des"];
  var now = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Jakarta" }));
  var hariIni = HARI[now.getDay()];
  var tanggal = now.getDate() + " " + BULAN[now.getMonth()] + " " + now.getFullYear();

  var todayLine = document.getElementById("today-line");
  if (todayLine) {
    todayLine.textContent = hariIni + ", " + tanggal + " WIB";
  }

  /* ——— sorot baris jadwal hari ini + catatan ——— */
  var rows = document.querySelectorAll("tr.mk-row");
  var mkHariIni = [];
  rows.forEach(function (row) {
    if (row.getAttribute("data-hari") === hariIni) {
      row.classList.add("today");
      mkHariIni.push(row.cells[2].textContent + " " +
                     row.cells[1].textContent);
    }
  });
  var note = document.getElementById("today-note");
  if (note) {
    if (mkHariIni.length) {
      note.textContent = "Hari ini (" + hariIni + "): " + mkHariIni.join(" · ");
    } else {
      note.textContent = "Hari ini (" + hariIni + "): tidak ada kuliah.";
    }
  }

  /* ——— filter entri log ——— */
  var buttons = document.querySelectorAll(".filters button");
  var entries = document.querySelectorAll(".log-entry");
  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      buttons.forEach(function (b) {
        b.classList.remove("active");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      var f = btn.getAttribute("data-filter");
      entries.forEach(function (entry) {
        var show = f === "semua" || entry.getAttribute("data-cat") === f;
        entry.classList.toggle("hidden", !show);
      });
    });
  });
})();
