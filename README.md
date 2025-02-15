# Novel Info Scraper

This Python program scrapes information about light novels specifically from [esnovels.com](https://esnovels.com/), including:
- Title, cover image, alternative title, status, type, genre, authors, artist, volume count, publisher, translation group, synopsis, and tags.
- EPUB download links for each volume.

For each EPUB found, it generates a Markdown file in the `~/obsidian/_inbox` directory with the format:
```
{Title} Volume {Number}.md
```

### Usage
```sh
python program.py <novel_url>
```

### Requirements
- Python 3.x
- Install dependencies with:
```sh
pip install requests-html beautifulsoup4
```

### Features
- Extracts and organizes novel metadata.
- Saves one Markdown file per volume with an `epubUrl` and `url` property.
- Handles spaces in file names automatically.
