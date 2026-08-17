#!/usr/bin/env node
// Real end-to-end test of docs/scan.html against the ACTUAL production
// Pyodide CDN (jsdelivr) -- not a local vendored copy, not a mock.
// This repository's own dev sandbox blocks cdn.jsdelivr.net at the
// network-policy level (same restriction that made the Groq features'
// live-verification workflows necessary), so this test can only run
// somewhere with normal internet access -- a GitHub Actions runner,
// or a developer's own machine. See
// .github/workflows/docs_scan_live_demo.yml.
//
// Usage:
//   node docs/tests/live_scan_test.mjs <base-url> <chromium-executable-path>
//
// <base-url> should be a running static server rooted at docs/ (e.g.
// http://127.0.0.1:8000/) -- this script does not start one itself.
// <chromium-executable-path> is optional; omit to use Playwright's
// own managed browser (requires `npx playwright install chromium`
// to have been run first).

import { chromium } from "playwright";
import assert from "node:assert/strict";

const baseUrl = process.argv[2];
const executablePath = process.argv[3] || undefined;
// Not part of this test's normal contract -- exists only so this
// script's own logic (not the real CDN, which the dev sandbox can't
// reach) can be dry-run locally against a vendored Pyodide copy before
// shipping a change here. Real CI runs never set this.
const pyodideBaseOverride = process.env.PYODIDE_BASE_OVERRIDE;

if (!baseUrl) {
  console.error("usage: node live_scan_test.mjs <base-url> [chromium-executable-path]");
  process.exit(2);
}

const CLEAN_SPECIMEN = {
  title: "Clean specimen (expect zero paper_rigor structural gaps)",
  // Short and plain on purpose -- below the disclaimer/limitations
  // word-count threshold, no placeholder phrases, no uncited stats.
  text: "This is a short, plain note about a distributed system's retry logic. " +
        "It describes the behavior without making any certainty claims or citing any statistics.",
};

const FLAGGED_SPECIMEN = {
  title: "Flagged specimen (expect real hits across multiple tools)",
  text: "It is trivial to show this conclusively demonstrates the result, beyond any doubt. " +
        "TODO: fill in proof. Research shows the approach is universally superior, achieving 99.7% accuracy. " +
        "This is a genuinely emergent capability nobody predicted.",
};

async function runScanOnPage(page, specimen) {
  await page.fill("#input-title", specimen.title);
  await page.fill("#input-text", specimen.text);
  await page.click("#scan-button");
  await page.waitForFunction(
    () => {
      const s = document.getElementById("status").textContent;
      return s === "Done." || s.startsWith("Error");
    },
    { timeout: 120_000 } // real CDN fetch + wasm boot, generous budget
  );
  const status = await page.locator("#status").textContent();
  assert.equal(status, "Done.", `scan did not complete cleanly: ${status}`);
  return page.locator("#report").innerHTML();
}

async function main() {
  const browser = await chromium.launch(executablePath ? { executablePath } : {});
  const consoleErrors = [];
  const failedRequests = [];

  try {
    const page = await browser.newPage({ viewport: { width: 1200, height: 1400 } });
    page.on("console", (msg) => {
      if (msg.type() === "error") consoleErrors.push(msg.text());
    });
    page.on("requestfailed", (req) => {
      // The browser's automatic favicon.ico probe 404s on every page in
      // this repo (no favicon declared) -- harmless, not part of this
      // feature's own network surface. Everything else failing here is
      // a real problem (the whole point of this test running against
      // the real CDN instead of a local vendored copy).
      if (!req.url().endsWith("/favicon.ico")) {
        failedRequests.push(req.url() + " :: " + (req.failure()?.errorText || "unknown"));
      }
    });

    const scanUrl = new URL("scan.html", baseUrl);
    if (pyodideBaseOverride) {
      scanUrl.searchParams.set("pyodide_base", pyodideBaseOverride);
    }
    console.log(`=== Loading scan.html (pyodide base: ${pyodideBaseOverride || "real jsdelivr CDN"}) ===`);
    await page.goto(scanUrl.href);

    console.log("=== Scan 1: clean specimen ===");
    const cleanHtml = await runScanOnPage(page, CLEAN_SPECIMEN);
    assert.ok(cleanHtml.includes("Paper-Rigor Scan Report"), "report heading missing");
    assert.ok(cleanHtml.includes("No defensive maneuvers flagged"), "expected attractor_scan clean read");
    assert.ok(cleanHtml.includes("no provisionalization"), "expected bifp clean read");
    console.log("  OK -- clean specimen produced a clean-shaped report");

    console.log("=== Scan 2: flagged specimen ===");
    const flaggedHtml = await runScanOnPage(page, FLAGGED_SPECIMEN);
    assert.ok(/Structural gaps:.*<strong>[1-9]/.test(flaggedHtml), "expected paper_rigor structural gaps > 0");
    assert.ok(flaggedHtml.includes("99.7%"), "expected the uncited statistic to surface");
    console.log("  OK -- flagged specimen produced real, non-zero findings");

    console.log("=== Discrimination check ===");
    assert.notEqual(cleanHtml, flaggedHtml, "clean and flagged specimens produced identical reports");
    console.log("  OK -- the two specimens read differently, not just a static template");

    console.log("=== Download buttons ===");
    const [mdDownload] = await Promise.all([
      page.waitForEvent("download"),
      page.click("#download-md"),
    ]);
    assert.equal(mdDownload.suggestedFilename(), "paper-rigor-report.md");
    const [jsonDownload] = await Promise.all([
      page.waitForEvent("download"),
      page.click("#download-json"),
    ]);
    assert.equal(jsonDownload.suggestedFilename(), "paper-rigor-report.json");
    console.log("  OK -- both downloads fire with the expected filenames");

    if (consoleErrors.length) {
      console.log("=== Browser console errors observed (informational) ===");
      for (const e of consoleErrors) console.log("  " + e);
    }
    if (failedRequests.length) {
      throw new Error("Unexpected failed network request(s):\n  " + failedRequests.join("\n  "));
    }

    console.log("\nAll live checks passed against the real Pyodide CDN.");
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error("\nLIVE SCAN TEST FAILED:", err.message);
  process.exit(1);
});
