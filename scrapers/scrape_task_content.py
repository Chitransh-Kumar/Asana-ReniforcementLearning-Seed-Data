import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

ASANA_URLS = [
    "https://asana.com/templates",
    "https://asana.com/guide/help/templates"
]

OUTPUT_DIR = Path("scrapers/cache")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[•●►]", "", text)
    return text.strip()


def is_valid_task_title(text: str) -> bool:
    return 6 <= len(text) <= 80 and text[0].isupper()


def is_valid_description(text: str) -> bool:
    return 20 <= len(text) <= 500


def scrape_asana():
    titles = set()
    descriptions = set()

    for url in ASANA_URLS:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Headings often resemble task names
        for tag in soup.find_all(["h3", "h4", "strong"]):
            text = clean(tag.get_text())
            if is_valid_task_title(text):
                titles.add(text)

        # Paragraphs resemble task descriptions
        for tag in soup.find_all("p"):
            text = clean(tag.get_text())
            if is_valid_description(text):
                descriptions.add(text)

    return titles, descriptions


def split_descriptions(descriptions):
    short_desc = []
    long_desc = []

    for d in descriptions:
        if len(d.split()) <= 25:
            short_desc.append(d)
        else:
            long_desc.append(d)

    return short_desc, long_desc


if __name__ == "__main__":
    titles, descriptions = scrape_asana()
    short_desc, long_desc = split_descriptions(descriptions)

    with open(OUTPUT_DIR / "asana_task_titles.json", "w", encoding="utf-8") as f:
        json.dump(sorted(titles), f, indent=2)

    with open(OUTPUT_DIR / "asana_task_descriptions_short.json", "w", encoding="utf-8") as f:
        json.dump(sorted(short_desc), f, indent=2)

    with open(OUTPUT_DIR / "asana_task_descriptions_long.json", "w", encoding="utf-8") as f:
        json.dump(sorted(long_desc), f, indent=2)

    print("Scraping complete:")
    print(f"Titles: {len(titles)}")
    print(f"Short descriptions: {len(short_desc)}")
    print(f"Long descriptions: {len(long_desc)}")
