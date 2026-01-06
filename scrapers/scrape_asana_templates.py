import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

URL = "https://asana.com/templates"
OUTPUT_PATH = Path("scrapers/cache/asana_project_templates.json")

def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def scrape_asana_templates():
    response = requests.get(URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    names = set()

    # Asana uses headings + cards
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = clean(tag.get_text())
        if 8 <= len(text) <= 80:
            names.add(text)

    return sorted(names)

if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    templates = scrape_asana_templates()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=2)

    print(f"Saved {len(templates)} Asana project templates")
