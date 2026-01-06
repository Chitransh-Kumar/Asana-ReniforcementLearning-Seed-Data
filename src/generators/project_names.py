import json
import random

with open("scrapers/cache/asana_project_templates.json") as f:
    ASANA_NAMES = json.load(f)

with open("scrapers/cache/saas_project_names.json") as f:
    SAAS_NAMES = json.load(f)

ALL_PROJECT_NAMES = ASANA_NAMES + SAAS_NAMES

def generate_project_name() -> str:
    return random.choice(ALL_PROJECT_NAMES)
