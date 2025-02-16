import os
import re

# Directory to save the markdown files
directory = os.path.expanduser('~/obsidian/_inbox')

# Function to prompt for input with a default value
def prompt_input(prompt_text, default=""):
    value = input(f"{prompt_text} [{default}]: ").strip()
    return value if value else default

# Escape special characters for Markdown
def escape_markdown(text):
    return text.replace("'", "\\'").replace('"', '\\"')

# Sanitize filenames by removing bad characters
def sanitize_filename(filename):
    # Remove any characters that are not allowed in filenames (like colons, slashes, etc.)
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)

# Gather data from the user
cover_url = prompt_input("Cover URL")
url = prompt_input("URL")
title = prompt_input("Title")
author = prompt_input("Author")
tags = input("Tags (comma separated): ").split(',')
tags = [tag.strip() for tag in tags if tag.strip()]  # Remove extra spaces and empty tags
num_volumes = int(prompt_input("Number of Volumes", "1"))

# Ensure the output directory exists
os.makedirs(directory, exist_ok=True)

# Create a file for each volume
for volume in range(1, num_volumes + 1):
    volume_title = f"{title} Volume {volume}"
    
    # Sanitize the filename to avoid bad characters
    sanitized_filename = sanitize_filename(f"{volume_title}.md")
    filename = os.path.join(directory, sanitized_filename)

    # Create the markdown content
    content = f"""---
coverUrl: {cover_url}
url: {url}
title: "{escape_markdown(volume_title)}"
author: "{escape_markdown(author)}"
tags:
"""

    for tag in tags:
        content += f"  - {tag}\n"

    content += "---\n"

    # Write to the file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Created: {filename}")

print("All files created successfully.")
