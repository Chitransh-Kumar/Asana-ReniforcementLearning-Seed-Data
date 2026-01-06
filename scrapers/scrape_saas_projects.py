import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

REPOS = [
    "https://github.com/vercel/vercel",
    "https://github.com/supabase/supabase",
    "https://github.com/stripe/stripe-cli",
    "https://github.com/hashicorp/terraform"
]

OUTPUT_PATH = Path("scrapers/cache/saas_project_names.json")

def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[#>*`]", "", text)
    return text.strip()

def scrape_repo_titles(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    titles = set()

    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = clean(tag.get_text())
        if 10 <= len(text) <= 80:
            titles.add(text)

    return titles

if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_titles = set()

    for repo in REPOS:
        try:
            all_titles.update(scrape_repo_titles(repo))
        except Exception:
            continue

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(all_titles), f, indent=2)

    print(f"Saved {len(all_titles)} SaaS project names")
