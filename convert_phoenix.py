import os
from pathlib import Path

SOURCE_DIR = Path("docs")
TARGET_DIR = Path("phoenix")

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Phoenix Document</title>

<script>
window.MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
    svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

<script>
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
</script>

<style>
:root {
    --bg: #0d0d0d;
    --fg: #ffffff;
    --fg-secondary: #e6e6e6;
    --link: #d0e0ff;
}
[data-theme="light"] {
    --bg: #ffffff;
    --fg: #222222;
    --fg-secondary: #555555;
    --link: #0050a0;
}
body {
    background: var(--bg);
    color: var(--fg);
    font-family: Segoe UI, Roboto, Helvetica, Arial, sans-serif;
    margin: 40px auto;
    max-width: 900px;
    line-height: 1.6;
}
a { color: var(--link); }
p { color: var(--fg-secondary); }
.theme-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--fg);
    color: var(--bg);
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    user-select: none;
}
</style>
</head>

<body>
<div class="theme-toggle" onclick="toggleTheme()">Toggle Theme</div>

<script>
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current == 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}
</script>
"""

HTML_FOOTER = """</body>
</html>
"""

def convert_markdown_to_html(md_text):
    lines = md_text.split("\n")
    out = []

    for line in lines:
        # headings
        if line.startswith("# "):
            out.append("<h1>" + line[2:] + "</h1>")
            continue
        if line.startswith("## "):
            out.append("<h2>" + line[3:] + "</h2>")
            continue
        if line.startswith("### "):
            out.append("<h3>" + line[4:] + "</h3>")
            continue
        if line.startswith("#### "):
            out.append("<h4>" + line[5:] + "</h4>")
            continue

        # links: [text](url)
        if "[" in line and "](" in line:
            parts = line.split("[")
            rebuilt = parts[0]
            for p in parts[1:]:
                if "](" in p:
                    text, rest = p.split("](", 1)
                    url, tail = rest.split(")", 1)
                    rebuilt += f'<a href="{url}">{text}</a>' + tail
                else:
                    rebuilt += p
            out.append(rebuilt)
            continue

        # normal line
        out.append(line)

    return HTML_HEADER + "<br>\n".join(out) + HTML_FOOTER

def process():
    if not SOURCE_DIR.exists():
        print("docs/ directory not found.")
        return

    TARGET_DIR.mkdir(exist_ok=True)

    for root, dirs, files in os.walk(SOURCE_DIR):
        rel = Path(root).relative_to(SOURCE_DIR)
        out_dir = TARGET_DIR / rel
        out_dir.mkdir(parents=True, exist_ok=True)

        for f in files:
            if f.endswith(".md"):
                src = Path(root) / f
                dst = out_dir / f.replace(".md", ".html")

                with open(src, "r", encoding="utf-8") as md:
                    text = md.read()

                html = convert_markdown_to_html(text)

                with open(dst, "w", encoding="utf-8") as out:
                    out.write(html)

                print("Converted:", src, "→", dst)

    print("\nPhoenix HTML conversion complete.")

if __name__ == "__main__":
    process()

