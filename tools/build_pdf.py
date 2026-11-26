"""Build the submission PDF from the deliverables (Markdown -> HTML -> PDF via headless Edge/Chrome).

Usage: python tools/build_pdf.py [browser.exe]
Output: deliverables/Fraga-v2-Quality-Strategy.pdf (plus build/*.html)
"""
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/GinoGalotti/FragaTest/blob/main/"
PARTS = ["deliverables/01-quality-strategy.md", "deliverables/02-evaluation-design.md",
         "harness/README.md", "deliverables/03-ai-usage.md"]
BROWSER = sys.argv[1] if len(sys.argv) > 1 else r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 14mm 14mm 16mm 14mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 9.5pt; line-height: 1.35; color: #1a1a1a; }
h1 { font-size: 16pt; color: #5b1a86; margin: 0 0 6px; }
h2 { font-size: 12pt; color: #5b1a86; margin: 12px 0 4px; border-bottom: 1px solid #ddd; }
h3 { font-size: 10.5pt; margin: 10px 0 4px; }
p, ul, ol { margin: 4px 0; }
table { border-collapse: collapse; width: 100%; margin: 6px 0; font-size: 8.5pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #ccc; padding: 3px 5px; vertical-align: top; text-align: left; }
th { background: #f3eef7; }
code, pre { font-family: Consolas, monospace; font-size: 8pt; }
pre { background: #f6f6f6; padding: 6px; white-space: pre-wrap; }
blockquote { margin: 4px 0; padding-left: 8px; border-left: 3px solid #ccc; color: #555; }
a { color: #5b1a86; text-decoration: none; }
.part { page-break-before: always; }
.part:first-child { page-break-before: avoid; }
.meta { color: #666; font-size: 8.5pt; margin-bottom: 8px; }
"""


def absolutise_links(md_text, src):
    """Relative repo links become GitHub links, so they work inside the PDF."""
    base = (ROOT / src).parent

    def fix(match):
        text, target = match.group(1), match.group(2)
        if re.match(r"^(https?:|#|mailto:)", target):
            return match.group(0)
        path = (base / target).resolve().relative_to(ROOT).as_posix()
        return "[%s](%s%s)" % (text, REPO, path)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", fix, md_text)


def render(parts):
    html = []
    for src in parts:
        text = absolutise_links((ROOT / src).read_text(encoding="utf-8"), src)
        html.append('<section class="part">%s</section>' % markdown.markdown(text, extensions=["tables", "fenced_code"]))
    return ("<!doctype html><html><head><meta charset='utf-8'><title>Fråga v2 Quality Strategy</title>"
            "<style>%s</style></head><body>%s</body></html>" % (CSS, "\n".join(html)))


def to_pdf(html, name):
    out_dir = ROOT / "build"
    out_dir.mkdir(exist_ok=True)
    html_path = out_dir / (name + ".html")
    html_path.write_text(html, encoding="utf-8")
    pdf_path = out_dir / (name + ".pdf")
    subprocess.run([BROWSER, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=%s" % pdf_path, html_path.as_uri()], check=True, timeout=120)
    pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf_path.read_bytes()))
    return pdf_path, pages


if __name__ == "__main__":
    _, strategy_pages = to_pdf(render(PARTS[:1]), "strategy-only")
    pdf, total = to_pdf(render(PARTS), "Fraga-v2-Quality-Strategy")
    final = ROOT / "deliverables" / "Fraga-v2-Quality-Strategy.pdf"
    final.write_bytes(pdf.read_bytes())
    print("Strategy: %d pages (limit 4). Full PDF: %d pages -> %s" % (strategy_pages, total, final.relative_to(ROOT)))
