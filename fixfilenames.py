import os
import re
import sys

# List of characters that are considered 'bad' for Android file names
BAD_CHARACTERS = r'[<>:"/\\|?*\x00-\x1F]'

# Function to check if a filename contains bad characters
def has_bad_characters(filename):
    return bool(re.search(BAD_CHARACTERS, filename))

# Function to fix the filename by removing bad characters
def fix_filename(filename):
    return re.sub(BAD_CHARACTERS, '', filename)

# Function to search for markdown files in the given directory
def search_and_fix_files(directory):
    # Traverse the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a markdown file
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                if has_bad_characters(file):
                    new_filename = fix_filename(file)
                    new_file_path = os.path.join(root, new_filename)
                    # Rename the file to fix bad characters
                    print(f"Renaming: {file_path} -> {new_file_path}")
                    os.rename(file_path, new_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_bad_filenames.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"The specified directory '{directory}' does not exist.")
        sys.exit(1)

    search_and_fix_files(directory)
    print("Done fixing bad filenames.")
