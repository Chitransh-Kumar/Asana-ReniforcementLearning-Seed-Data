# Asana RL Seed Data Simulation

This repository contains a **high-fidelity synthetic dataset** that simulates how a large **B2B SaaS organization** uses **Asana** for day-to-day work management.

The dataset is designed as **seed data for reinforcement learning (RL) environments** used to evaluate and fine-tune **computer-use AI agents** operating inside enterprise productivity tools.

The primary focus of this project is **behavioral realism**, not replication of Asana’s internal production schema.

---

## Key Highlights

- Simulates a mature B2B SaaS organization with **5,000–10,000 users**
- Realistic organizational hierarchy with teams and **matrix memberships**
- Project-scoped workflows and ordered sections
- Non-uniform task distributions (unassigned tasks, missing due dates, incomplete work)
- Single-level subtasks with strict temporal constraints
- **Web-scraped content (one-time)** for:
  - User names
  - Project names
  - Task titles and descriptions
- Controlled fallback logic to ensure deterministic generation
- **Offline, reproducible pipeline**
- No runtime API keys or live network calls during generation

---

## Repository Structure

```
asana-rl-seed-data/
├── README.md
├── requirements.txt
├── schema.sql
├── .env.example
│
├── scrapers/
│   ├── __init__.py
│   ├── names.py
│   ├── scrape_task_content.py
│   └── cache/
│       ├── asana_task_titles.json
│       ├── asana_task_descriptions_short.json
│       └── asana_task_descriptions_long.json
│
├── src/
│   ├── main.py
│   ├── config/
│   ├── db/
│   ├── generators/
│   ├── utils/
│   └── constants/
│
├── prompts/
│   ├── comments.txt
│   ├── generated_comments.txt
│   ├── tags.txt
│   └── generated_tags.txt
│
└── output/
    └── asana_simulation.sqlite
```

---

## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. (Optional) Run one-time web scraping

```bash
python scrapers/scrape_task_content.py
```

---

### 3. Generate the dataset

```bash
python src/main.py
```

The final database will be written to:

```
output/asana_simulation.sqlite
```

---

## Web Scraping Strategy

Web scraping is used **only as a one-time data source**. All scraped content is cached locally and reused during generation to ensure reproducibility.

---

## LLM Usage (Offline & Cached)

LLMs are used **only offline** to generate task comments and tag vocabularies. Outputs are cached and sampled during generation.

---

## Data Model Overview

The dataset models:

- organizations
- teams
- users
- team_memberships
- projects
- sections
- tasks
- subtasks
- comments
- tags
- task_tags
- custom_field_definitions
- custom_field_values

---

## Design Principles

- UUIDv4 identifiers
- Strict temporal and relational consistency
- Intentional sparsity and skewed distributions
- Clear separation between scraping, generation, and schema

---

## Output

```
output/asana_simulation.sqlite
```

Ready for RL simulation and downstream evaluation.

---

## License

Provided for evaluation and educational purposes only.
