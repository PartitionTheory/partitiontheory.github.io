import os
import markdown

INPUT_DIR = "docs"
OUTPUT_DIR = "phoenix"

# Detect epoch directory from filename pattern
def detect_epoch_from_filename(filename):
    # PHOENIX-EPOCH-8-FOUNDATION.md → epoch8
    if filename.startswith("PHOENIX-EPOCH-"):
        parts = filename.split("-")
        epoch_number = parts[2]  # "8"
        return f"epoch{epoch_number}"
    return None

# Rewrite markdown links into correct HTML links
def rewrite_links(line):
    if "[" not in line or "](" not in line:
        return line

    out = ""
    parts = line.split("[")

    out += parts[0]

    for p in parts[1:]:
        if "](" in p:
            text, rest = p.split("](", 1)
            url, tail = rest.split(")", 1)

            # .md → .html
            if url.endswith(".md"):
                html_name = url[:-3] + ".html"

                # detect epoch directory
                epoch_dir = detect_epoch_from_filename(url)

                if epoch_dir:
                    url = f"{epoch_dir}/{html_name}"
                else:
                    url = html_name

            out += f'<a href="{url}">{text}</a>' + tail
        else:
            out += p

    return out

PHOENIX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Phoenix</title>

<link rel="stylesheet" href="/phoenix/phoenix.css">

<script>
function toggleTheme() {
    const body = document.body;
    const theme = body.dataset.theme === "dark" ? "light" : "dark";
    body.dataset.theme = theme;
    localStorage.setItem("phoenix-theme", theme);
}
window.onload = () => {
    const saved = localStorage.getItem("phoenix-theme") || "dark";
    document.body.dataset.theme = saved;
};
</script>

<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

</head>

<body>

<div id="nav">
    <a href="/phoenix/index.html">Index</a> |
    <a href="#" onclick="window.scrollTo(0,0)">Top</a> |
    <a href="#" onclick="window.scrollTo(0,document.body.scrollHeight)">Bottom</a> |
    <button onclick="toggleTheme()">Toggle Theme</button>
</div>

<div id="content">
{{CONTENT}}
</div>

</body>
</html>
"""

# Convert a single markdown file to HTML
def convert_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    processed = [rewrite_links(line) for line in lines]
    inner_html = markdown.markdown("".join(processed), extensions=["tables", "fenced_code"])

    full_html = PHOENIX_TEMPLATE.replace("{{CONTENT}}", inner_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

# Ensure output directory exists
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Main conversion routine
def convert_all():
    ensure_dir(OUTPUT_DIR)

    for root, dirs, files in os.walk(INPUT_DIR):
        rel = os.path.relpath(root, INPUT_DIR)

        # Output directory mirrors input directory
        out_dir = os.path.join(OUTPUT_DIR, rel)
        ensure_dir(out_dir)

        for file in files:
            if file.endswith(".md"):
                input_path = os.path.join(root, file)
                output_name = file[:-3] + ".html"
                output_path = os.path.join(out_dir, output_name)

                convert_file(input_path, output_path)

if __name__ == "__main__":
    convert_all()

