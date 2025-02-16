import os
import re

def fix_tags_in_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    in_front_matter = False
    in_tags_section = False
    tags_buffer = []
    new_lines = []
    changed = False

    for line in lines:
        stripped_line = line.strip()

        # Toggle front matter detection
        if stripped_line == '---':
            if in_front_matter:
                in_front_matter = False
                in_tags_section = False

                # Fix broken "Slice of Life" tags
                i = 0
                while i < len(tags_buffer) - 2:
                    if tags_buffer[i:i+3] == ['Slice', 'of', 'Life']:
                        tags_buffer = tags_buffer[:i] + ['Slice-Of-Life'] + tags_buffer[i+3:]
                        changed = True
                    i += 1

                # Only add tags section if there were tags collected
                if tags_buffer:
                    new_lines.append("tags:\n")
                    for tag in tags_buffer:
                        new_lines.append(f"  - {tag}\n")
                    tags_buffer = []

            else:
                in_front_matter = True
                in_tags_section = False

        # Check for bad format tags (e.g., tags: ['Romance', 'Comedy'])
        if in_front_matter and stripped_line.startswith('tags: ['):
            in_tags_section = False  # Disable normal tags section processing

            # Extract the tags inside the brackets
            tags_content = re.search(r"tags:\s*\[(.*)\]", stripped_line)
            if tags_content:
                tags = tags_content.group(1).split(',')
                cleaned_tags = []

                for tag in tags:
                    # Clean and fix tags by stripping quotes and replacing spaces with hyphens
                    tag = tag.strip().strip("'\"")
                    tag = re.sub(r'\s+', '-', tag)
                    cleaned_tags.append(tag)

                # Collect tags for writing later
                tags_buffer.extend(cleaned_tags)
                changed = True
                continue

        # Detect proper tags section
        if in_front_matter and stripped_line.startswith('tags:'):
            in_tags_section = True
            continue  # Skip the current line to avoid duplicate "tags:"

        elif in_tags_section:
            if stripped_line.startswith('- '):
                tag = stripped_line[2:].strip()
                # Replace spaces with hyphens
                new_tag = re.sub(r'\s+', '-', tag)
                if new_tag != tag:
                    changed = True
                tags_buffer.append(new_tag)
                continue
            else:
                in_tags_section = False

                # Fix broken "Slice of Life" tags
                i = 0
                while i < len(tags_buffer) - 2:
                    if tags_buffer[i:i+3] == ['Slice', 'of', 'Life']:
                        tags_buffer = tags_buffer[:i] + ['Slice-Of-Life'] + tags_buffer[i+3:]
                        changed = True
                    i += 1

                # Only add tags section if there were tags collected
                if tags_buffer:
                    new_lines.append("tags:\n")
                    for tag in tags_buffer:
                        new_lines.append(f"  - {tag}\n")
                    tags_buffer = []

        new_lines.append(line)

    # Only overwrite file and print if changes were made
    if changed:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"Modified: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                fix_tags_in_file(file_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python program.py <directory>")
    else:
        directory = sys.argv[1]
        process_directory(directory)

