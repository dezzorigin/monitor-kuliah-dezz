import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  fullyParallel: true,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:8470",
  },
  webServer: {
    command: "python3 -m http.server 8470 --directory landing",
    url: "http://127.0.0.1:8470/",
    reuseExistingServer: true,
    timeout: 10_000,
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile", use: { ...devices["iPhone 13"] } },
  ],
});
