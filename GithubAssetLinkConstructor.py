import html
from pathlib import Path

IMAGE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif",
    ".bmp", ".webp", ".svg"
}

AUDIO_EXTS = {
    ".mp3", ".wav", ".ogg",
    ".m4a", ".aac", ".flac"
}

mypath = Path.cwd()

github_site = ""
for part in mypath.parts:
    if ".github.io" in part:
        github_site = part
        break

if not github_site:
    github_site = "yourname.github.io"


SUPPORTED_EXTS = IMAGE_EXTS | AUDIO_EXTS

files = sorted(
    [
        f for f in mypath.rglob("*")
        if (
            f.is_file()
            and f.name != "index.html"
            and f.suffix.lower() in SUPPORTED_EXTS
        )
    ],
    key=lambda p: str(p).lower()
)


fileOutput = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Repository File Index</title>

<style>
body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 30px;
    background: #f5f5f5;
}

h2 {
    margin-top: 0;
}

#searchBox {
    width: 100%;
    max-width: 600px;
    padding: 10px;
    font-size: 16px;
    margin-bottom: 20px;
}

.file {
    background: white;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,.08);
}

.file a {
    word-break: break-all;
}

details {
    margin-top: 10px;
}

img {
    margin-top: 10px;
    max-width: 500px;
    max-height: 500px;
    border: 1px solid #ccc;
}

button {
    margin-left: 10px;
    padding: 5px 10px;
    cursor: pointer;
}

button:disabled {
    opacity: 0.7;
}
</style>

</head>
<body>

<h2>Repository Files</h2>

<input
    id="searchBox"
    type="text"
    placeholder="Search files..."
    onkeyup="filterFiles()"
/>

<div id="fileList">
"""

# -----------------------------
# Generate entries
# -----------------------------

for f in files:

    relative_path = f.relative_to(mypath).as_posix()
    url_path = relative_path.replace(" ", "%20")
    full_url = f"https://{github_site}/{url_path}"

    safe_name = html.escape(relative_path)
    safe_url = html.escape(full_url)

    ext = f.suffix.lower()

    fileOutput += f"""
<div class="file" data-name="{safe_name.lower()}">

<a href="{safe_url}">{safe_url}</a>

<button
    class="copyBtn"
    onclick="copyUrl('{safe_url}', this)">
    Copy URL
</button>
"""

    if ext in IMAGE_EXTS:

        fileOutput += f"""
<details>
<summary>Preview Image</summary>

<img
    src="{safe_url}"
    loading="lazy"
    alt="{safe_name}">

</details>
"""

    elif ext in AUDIO_EXTS:

        fileOutput += f"""
<button onclick="playPreview(this)">
Play 10s Preview
</button>

<audio preload="none">
<source src="{safe_url}">
</audio>
"""

    fileOutput += """
</div>
"""

# -----------------------------
# Scripts
# -----------------------------

fileOutput += """
</div>

<script>

function filterFiles() {

    const search =
        document.getElementById("searchBox")
        .value
        .toLowerCase();

    const files =
        document.getElementsByClassName("file");

    for (const file of files) {

        if (file.dataset.name.includes(search)) {
            file.style.display = "";
        } else {
            file.style.display = "none";
        }
    }
}

function copyUrl(url, button) {

    if (navigator.clipboard && window.isSecureContext) {

        navigator.clipboard.writeText(url)
            .then(() => flashCopied(button));

    } else {

        const textArea = document.createElement("textarea");
        textArea.value = url;

        document.body.appendChild(textArea);

        textArea.select();
        document.execCommand("copy");

        document.body.removeChild(textArea);

        flashCopied(button);
    }
}

function flashCopied(button) {

    const original = button.textContent;

    button.textContent = "Copied!";
    button.disabled = true;

    setTimeout(() => {
        button.textContent = original;
        button.disabled = false;
    }, 1200);
}

function playPreview(button) {

    const audio = button.nextElementSibling;

    document.querySelectorAll("audio").forEach(a => {

        if (a !== audio) {
            a.pause();
            a.currentTime = 0;
            clearTimeout(a.previewTimeout);
        }

    });

    audio.currentTime = 0;
    audio.play();

    clearTimeout(audio.previewTimeout);

    audio.previewTimeout = setTimeout(() => {
        audio.pause();
        audio.currentTime = 0;
    }, 10000);
}

</script>

</body>
</html>
"""


output_file = mypath / "index.html"
output_file.write_text(fileOutput, encoding="utf-8")

print(f"Success! Generated index.html with {len(files)} links.")
