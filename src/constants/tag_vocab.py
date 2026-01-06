from pathlib import Path

TAGS_FILE = Path("prompts/generated_tags.txt")

def load_tag_vocab():
    # Loads externally generated tag vocabulary with a small deterministic fallback
    if TAGS_FILE.exists():
        return [
            line.strip()
            for line in TAGS_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    return [
        "high-priority",
        "blocked",
        "bug",
        "enhancement",
        "tech-debt"
    ]

TAG_VOCAB = load_tag_vocab()
