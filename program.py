import sys
import os
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

def get_novel_info(url):
    session = HTMLSession()
    response = session.get(url)
    response.html.render()
    soup = BeautifulSoup(response.html.html, 'html.parser')

    title = soup.find('h3', {'id': 'title'}).text.strip()
    cover = soup.find('img', {'id': 'cover'})['src']
    alternative_title = soup.find('p', {'id': 'alternative'}).text.strip()
    status = soup.find('p', {'id': 'status'}).text.strip()
    type_ = soup.find('p', {'id': 'type'}).text.strip()
    genre = soup.find('p', {'id': 'genre'}).text.strip()
    tags = [tag.strip() for tag in genre.split(',')]
    authors = soup.find('p', {'id': 'authors'}).text.strip()
    artist = soup.find('p', {'id': 'artist'}).text.strip()
    volume_count = soup.find('p', {'id': 'volumeCount'}).text.strip()
    publisher = soup.find('p', {'id': 'publisher'}).text.strip()
    translation_group = soup.find('p', {'id': 'translationGroup'}).text.strip()
    synopsis = soup.find('p', {'id': 'synopsis'}).text.strip()

    # Extract EPUB links and their volume numbers
    epub_links = []
    vol_sections = soup.find_all('p', {'id': 'vol'})
    for vol in vol_sections:
        # Extract volume number from the text
        volume_number = re.search(r'Volume (\d+)', vol.text, re.IGNORECASE)
        volume_number = volume_number.group(1) if volume_number else "Unknown"

        # Find the EPUB link in the same section
        epub_link = vol.find('a', string='Epub')
        if epub_link:
            epub_links.append((volume_number, epub_link['href']))

    return {
        "title": title,
        "cover": cover,
        "alternativeTitle": alternative_title,
        "status": status,
        "type": type_,
        "genre": genre,
        "tags": tags,
        "authors": authors,
        "artist": artist,
        "volumeCount": volume_count,
        "publisher": publisher,
        "translationGroup": translation_group,
        "synopsis": synopsis,
        "epubLinks": epub_links
    }

def generate_markdown(info, volume_number, epub_url, source_url):
    tags_formatted = "\n  - ".join(info['tags'])
    markdown_content = f"""---
title: "{info['title']} Volume {volume_number}"
coverUrl: {info['cover']}
alternativeTitle: "{info['alternativeTitle']}"
status: "{info['status']}"
type: "{info['type']}"
genre: "{info['genre']}"
authors: "{info['authors']}"
artist: "{info['artist']}"
volumeCount: "{info['volumeCount']}"
publisher: "{info['publisher']}"
translationGroup: "{info['translationGroup']}"
synopsis: "{info['synopsis']}"
tags:
  - {tags_formatted}
epubUrl: {epub_url}
url: {source_url}
---
"""
    return markdown_content

def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py <novel_url>")
        sys.exit(1)

    url = sys.argv[1]
    info = get_novel_info(url)

    # Define the save directory and ensure it exists
    save_dir = os.path.expanduser('~/obsidian/_inbox')
    os.makedirs(save_dir, exist_ok=True)

    # Create a file for each EPUB link found
    for volume_number, epub_url in info['epubLinks']:
        # Create Markdown content for each volume
        markdown_content = generate_markdown(info, volume_number, epub_url, url)

        # Generate the filename and save the Markdown file
        file_name = f"{info['title']} Volume {volume_number}.md"
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        print(f"Markdown file saved as {file_path}")

if __name__ == "__main__":
    main()

