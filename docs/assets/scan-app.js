// Drives docs/scan.html: boots Pyodide, installs the 5 scanner wheels
// via micropip, runs assets/py/paper_scan.py's aggregator against
// user-supplied text, and renders the resulting report. The scanned
// text never leaves this tab -- the only network requests this file
// makes are for the Pyodide runtime and this repo's own wheel files,
// both static assets, never the input text.
//
// PYODIDE_BASE defaults to the jsdelivr CDN. Overridable via a
// ?pyodide_base= query param purely so this exact code path can be
// tested against a locally-served Pyodide copy in environments where
// the CDN itself is unreachable (this repo's own dev sandbox blocks
// it at the network-policy level) -- production visitors never set
// this param and always get the CDN.
const PYODIDE_BASE = new URLSearchParams(location.search).get("pyodide_base")
  || "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";

const WHEELS = [
  "assets/wheels/verification_lint-0.1.0-py3-none-any.whl",
  "assets/wheels/paper_rigor-0.1.0-py3-none-any.whl",
  "assets/wheels/attractor_scan-0.1.0-py3-none-any.whl",
  "assets/wheels/bifp-0.1.0-py3-none-any.whl",
  "assets/wheels/debasinizer-0.1.0-py3-none-any.whl",
];

let pyodideReadyPromise = null;
let paperScanModule = null;

function setStatus(message, isError) {
  const el = document.getElementById("status");
  if (!el) return;
  el.textContent = message;
  el.classList.toggle("error", Boolean(isError));
}

function loadScriptTag(src) {
  return new Promise((resolve, reject) => {
    const tag = document.createElement("script");
    tag.src = src;
    tag.onload = () => resolve();
    tag.onerror = () => reject(new Error("Failed to load " + src));
    document.head.appendChild(tag);
  });
}

async function bootPyodide() {
  if (pyodideReadyPromise) return pyodideReadyPromise;

  pyodideReadyPromise = (async () => {
    setStatus("Loading Python runtime (Pyodide) -- one-time download, cached after...");
    await loadScriptTag(PYODIDE_BASE + "pyodide.js");
    const pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });

    setStatus("Loading micropip...");
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");

    setStatus("Installing scanner packages (verification_lint, paper_rigor, attractor_scan, bifp, debasinizer)...");
    const wheelUrls = WHEELS.map((w) => new URL(w, location.href).href);
    await micropip.install(wheelUrls);

    setStatus("Loading the aggregator...");
    const scriptResponse = await fetch(new URL("assets/py/paper_scan.py", location.href));
    if (!scriptResponse.ok) {
      throw new Error("Could not fetch assets/py/paper_scan.py (" + scriptResponse.status + ")");
    }
    const scriptText = await scriptResponse.text();
    pyodide.FS.writeFile("/home/pyodide/paper_scan.py", scriptText);
    paperScanModule = pyodide.pyimport("paper_scan");

    return pyodide;
  })();

  return pyodideReadyPromise;
}

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function inlineMarkdown(s) {
  let out = escapeHtml(s);
  out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  return out;
}

// Hand-rolled, on purpose: this only ever needs to render the small,
// fixed markdown subset paper_scan.py's generate_markdown_report()
// emits (#/##/### headings, **bold**, `code`, [links](url), single-
// and double-indented "- " bullets, blank-line paragraphs) -- pulling
// in a general markdown library would be the first external JS
// dependency in a project that otherwise has none, for a rendering
// job this constrained.
function markdownToHtml(markdown) {
  const lines = markdown.split("\n");
  let html = "";
  let listDepth = 0;

  function closeLists(toDepth) {
    while (listDepth > toDepth) {
      html += "</ul>";
      listDepth -= 1;
    }
  }

  for (const line of lines) {
    const headingMatch = line.match(/^(#{1,3})\s+(.*)$/);
    if (headingMatch) {
      closeLists(0);
      const level = headingMatch[1].length + 1; // offset: page already has its own <h1>
      html += `<h${level}>${inlineMarkdown(headingMatch[2])}</h${level}>`;
      continue;
    }

    const bulletMatch = line.match(/^(\s*)-\s+(.*)$/);
    if (bulletMatch) {
      const depth = bulletMatch[1].length >= 2 ? 2 : 1;
      if (listDepth < depth) {
        while (listDepth < depth) {
          html += "<ul>";
          listDepth += 1;
        }
      } else if (listDepth > depth) {
        closeLists(depth);
      }
      html += `<li>${inlineMarkdown(bulletMatch[2])}</li>`;
      continue;
    }

    closeLists(0);
    if (line.trim() === "") continue;
    html += `<p>${inlineMarkdown(line)}</p>`;
  }
  closeLists(0);
  return html;
}

function download(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

let lastMarkdown = "";
let lastJson = "";

async function runScan() {
  const text = document.getElementById("input-text").value.trim();
  const title = document.getElementById("input-title").value.trim();
  const scanButton = document.getElementById("scan-button");
  const reportEl = document.getElementById("report");
  const downloadsEl = document.getElementById("downloads");

  if (!text) {
    setStatus("Paste or upload some text first.", true);
    return;
  }

  scanButton.disabled = true;
  reportEl.innerHTML = "";
  downloadsEl.hidden = true;

  try {
    await bootPyodide();
    setStatus("Scanning...");

    const combined = paperScanModule.run_all_scans.callKwargs(text, { title: title });
    const markdown = paperScanModule.generate_markdown_report(combined);
    const jsonText = paperScanModule.report_as_json(combined);

    lastMarkdown = markdown;
    lastJson = jsonText;
    combined.destroy();

    reportEl.innerHTML = markdownToHtml(markdown);
    downloadsEl.hidden = false;
    setStatus("Done.");
  } catch (err) {
    console.error(err);
    setStatus("Error: " + err.message, true);
  } finally {
    scanButton.disabled = false;
  }
}

document.getElementById("scan-button").addEventListener("click", runScan);

document.getElementById("file-input").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const text = await file.text();
  document.getElementById("input-text").value = text;
  if (!document.getElementById("input-title").value) {
    document.getElementById("input-title").value = file.name.replace(/\.(txt|md)$/i, "");
  }
});

document.getElementById("download-md").addEventListener("click", () => {
  download("paper-rigor-report.md", lastMarkdown, "text/markdown");
});

document.getElementById("download-json").addEventListener("click", () => {
  download("paper-rigor-report.json", lastJson, "application/json");
});
