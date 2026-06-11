import os
from pathlib import Path

# 1. Get the current working directory (automatically handles \ or / based on OS)
mypath = Path.cwd()

# 2. Dynamically find the GitHub pages site name from the path
# This replaces the brittle string slicing from the original script
github_site = ""
for part in mypath.parts:
    if ".github.io" in part:
        github_site = part
        break

# Fallback in case the script is run outside the repo folder during testing
if not github_site:
    github_site = "yourname.github.io"

# 3. Recursively find all files using pathlib's cross-platform glob
# Change '*.*' to whatever extension you want to filter by if needed
files = list(mypath.rglob("*.*"))

fileOutput = '<body>\n'

for f in files:
    # Ensure we are only linking files, not directories, and skip index.html itself
    if f.is_file() and f.name != 'index.html':
        
        # .relative_to(mypath) strips the local machine's absolute path
        # .as_posix() FORCE-converts all backslashes to forward slashes for the URL
        relative_path = f.relative_to(mypath).as_posix()
        
        # URL encode spaces so links don't break
        url_path = relative_path.replace(' ', '%20')
        
        # Construct the web URL
        full_url = f"https://{github_site}/{url_path}"
        
        fileOutput += f'<a href="{full_url}">{full_url}</a> <br />\n'
	
fileOutput += '</body>'

# 4. Write out the file using UTF-8 encoding (works perfectly on both OS)
output_file = mypath / 'index.html'
output_file.write_text(fileOutput, encoding="utf-8")

print(f"Success! Generated index.html with {len(files)} links.")
