import os
import re

def fix_tags_in_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    in_front_matter = False
    in_tags_section = False
    new_lines = []

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Toggle front matter detection
        if stripped_line == '---':
            if in_front_matter:
                in_front_matter = False
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
                    cleaned_tags.append(f"  - {tag}")

                # Replace the bad tags line with the fixed format
                new_lines.append("tags:\n")
                new_lines.extend([tag + "\n" for tag in cleaned_tags])
                continue

        # Detect proper tags section
        if in_front_matter and stripped_line.startswith('tags:'):
            in_tags_section = True
            new_lines.append(line)
            continue
        elif in_tags_section:
            if stripped_line.startswith('- '):
                # Fix tags by replacing spaces with hyphens
                fixed_tag = re.sub(r'\s+', '-', stripped_line[2:])
                new_lines.append(f"  - {fixed_tag}\n")
                continue
            else:
                in_tags_section = False

        new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                fix_tags_in_file(file_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python program.py <directory>")
    else:
        directory = sys.argv[1]
        process_directory(directory)

