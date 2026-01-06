# src/generators/task_content.py
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ASANA_TITLES_PATH = BASE_DIR / "scrapers" / "cache" / "asana_task_titles.json"
SHORT_DESC_PATH = BASE_DIR / "scrapers" / "cache" / "asana_task_descriptions_short.json"
LONG_DESC_PATH = BASE_DIR / "scrapers" / "cache" / "asana_task_descriptions_long.json"


def load_json(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


TASK_TITLES = load_json(ASANA_TITLES_PATH)
SHORT_DESCRIPTIONS = load_json(SHORT_DESC_PATH)
LONG_DESCRIPTIONS = load_json(LONG_DESC_PATH)


# --- SAFE FALLBACKS (used only if scraped pools are empty) ---

FALLBACK_TITLES = [
    "Review implementation details",
    "Prepare release checklist",
    "Coordinate with stakeholders",
    "Validate feature requirements",
    "Resolve reported issues"
]

FALLBACK_SHORT_DESCRIPTIONS = [
    "Review the task requirements and confirm scope.",
    "Coordinate with relevant stakeholders to proceed.",
    "Validate current implementation against expectations.",
    "Ensure all dependencies are unblocked."
]

FALLBACK_LONG_DESCRIPTIONS = [
    "Review the task in detail and validate all functional and non-functional requirements. "
    "Coordinate with dependent teams if clarification is required. "
    "Document findings and next steps clearly in the task comments.",

    "This task involves multiple steps including analysis, implementation, validation, and handoff. "
    "Ensure alignment with the broader project goals and flag any risks early."
]


def generate_task_title():
    pool = TASK_TITLES if TASK_TITLES else FALLBACK_TITLES
    return random.choice(pool)


def generate_task_description():
    r = random.random()

    # 20% empty
    if r < 0.20:
        return None

    # 50% short
    if r < 0.70:
        pool = SHORT_DESCRIPTIONS if SHORT_DESCRIPTIONS else FALLBACK_SHORT_DESCRIPTIONS
        return random.choice(pool)

    # 30% long
    pool = LONG_DESCRIPTIONS if LONG_DESCRIPTIONS else FALLBACK_LONG_DESCRIPTIONS
    return random.choice(pool)
