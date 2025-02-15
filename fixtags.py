import os
import sys
import re

def fix_tags_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    in_properties = False
    new_lines = []

    for line in lines:
        if line.strip() == '---': 
            in_properties = not in_properties
        
        if in_properties and line.strip().startswith('- '): 
            # Check if it's a tag line and replace spaces with hyphens
            fixed_line = re.sub(r'- (.+)', lambda m: f"- {m.group(1).replace(' ', '-')}", line)
            new_lines.append(fixed_line)
        else:
            new_lines.append(line)

    # Save changes
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                fix_tags_in_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_tags.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Error: Provided path is not a directory.")
        sys.exit(1)
    
    process_directory(directory)

