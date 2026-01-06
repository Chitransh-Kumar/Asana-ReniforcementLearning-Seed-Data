# Asana RL Seed Data Simulation

This repository contains a high-fidelity synthetic dataset that simulates how a large B2B SaaS organization uses **Asana** for day-to-day work management.
The dataset is designed as **seed data for reinforcement learning (RL) environments** used to evaluate and fine-tune computer-use AI agents.

The focus of this project is **behavioral realism**, not replication of Asana’s internal production schema.

---

## Key Highlights

- Simulates a mature B2B SaaS organization with **5,000–10,000 users**
- Realistic organizational structure with teams and matrix memberships
- Project-specific workflows and sections
- Non-uniform task distributions (unassigned, overdue, incomplete tasks)
- Single-level subtasks with strict temporal consistency
- **LLM-assisted generation** for comments and tag vocabulary
- Fully reproducible and deterministic
- **No runtime API keys required**

---

## Repository Structure

```
asana-rl-seed-data/
├── README.md
├── requirements.txt
├── schema.sql
├── .env.example
├── src/
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   ├── db/
│   │   ├── connection.py
│   │   └── migrate.py
│   ├── generators/
│   │   ├── organizations.py
│   │   ├── teams.py
│   │   ├── users.py
│   │   ├── team_memberships.py
│   │   ├── projects.py
│   │   ├── sections.py
│   │   ├── tasks.py
│   │   ├── subtasks.py
│   │   ├── comments.py
│   │   ├── tags.py
│   │   ├── task_tags.py
│   │   ├── custom_field_definitions.py
│   │   └── custom_field_values.py
│   ├── utils/
│   │   ├── uuid.py
│   │   └── dates.py
│   └── constants/
│       ├── roles.py
│       ├── names.py
│       ├── workflows.py
│       ├── project_types.py
│       ├── project_names.py
│       ├── task_templates.py
│       ├── subtask_templates.py
│       ├── comment_templates.py
│       ├── tag_vocab.py
│       └── custom_fields.py
├── prompts/
│   ├── comments.txt
│   ├── generated_comments.txt
│   ├── tags.txt
│   └── generated_tags.txt
└── output/
    └── asana_simulation.sqlite
```

---

## Setup Instructions

### 1. Install dependencies

```
pip install -r requirements.txt
```

> Note: The project relies almost entirely on Python standard libraries.
> No heavy external dependencies are required.

---

### 2. Generate the dataset

```
python src/main.py
```

This will:
- Recreate the SQLite database
- Apply schema migrations
- Generate realistic seed data across all entities

The final database is written to:

```
output/asana_simulation.sqlite
```

---

## LLM Usage (Reproducible by Design)

LLMs are used **only offline** to generate:
- Task comment text
- Tag vocabulary

### How it works

- Prompt templates are stored in:
  - `prompts/comments.txt`
  - `prompts/tags.txt`
- LLM outputs are generated once and cached in:
  - `prompts/generated_comments.txt`
  - `prompts/generated_tags.txt`
- During data generation, the pipeline samples from cached outputs

### Important Guarantees

- No live API calls during execution
- No API keys required
- Fully deterministic and reproducible runs

---

## Data Model Overview

The dataset models the following core entities:
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

## Custom Fields

- Scoped per project
- Vary by project type
- Partially populated to reflect real-world usage

---

## Design Principles

- UUIDv4 identifiers for all primary keys
- Strict foreign-key and temporal consistency
- Skewed, non-uniform distributions by design
- Partial and missing metadata is intentional
- Clear separation between:
  - schema
  - generation logic
  - content generation (LLM prompts)

---

## Output

The final dataset is stored as a SQLite database:

```
output/asana_simulation.sqlite
```

This database is ready for:
- RL environment simulation
- behavioral analysis
- downstream evaluation pipelines

---

## Notes

This project is intentionally scoped for clarity, realism, and reproducibility.
Advanced Asana features outside core RL evaluation needs are omitted by design.

---

## License

This project is provided for evaluation and educational purposes only.
