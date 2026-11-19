import { expect, test } from "@playwright/test";

test("landing: judul + linimasa log + jadwal 13 MK", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(
    "Monitor Kuliah Dezz — Buku Log Arsip Absensi",
  );
  await expect(
    page.getByRole("heading", { name: "Linimasa entri" }),
  ).toBeVisible();
  await expect(page.locator("article.log-entry")).toHaveCount(8);
  await expect(page.locator("tr.mk-row")).toHaveCount(13);
  await expect(page.getByText("21 SKS").first()).toBeVisible();
  await expect(page.getByText("SINF2023").first()).toBeVisible();
  // stempel HADIR terlihat
  await expect(page.locator(".stamp.hadir").first()).toBeVisible();
  // og-image bisa dimuat
  const og = await page.request.get("/og-image.png");
  expect(og.status()).toBe(200);
  expect(og.headers()["content-type"]).toContain("image/");
});

test("landing: filter log menyaring entri", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Tugas" }).click();
  await expect(page.locator("article.log-entry:not(.hidden)")).toHaveCount(5);
  await expect(
    page.locator('article.log-entry[data-cat="absensi"]:not(.hidden)'),
  ).toHaveCount(0);
  await page.getByRole("button", { name: "Semua" }).click();
  await expect(page.locator("article.log-entry:not(.hidden)")).toHaveCount(8);
});

test("landing: mobile 390px tanpa scroll horizontal", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBe(0);
  await expect(page.locator("article.log-entry").first()).toBeVisible();
});
