from pathlib import Path

COMMENTS_FILE = Path("prompts/generated_comments.txt")

def load_comment_templates():
    # Loads externally generated comment text if available, with a small fallback set
    if COMMENTS_FILE.exists():
        return [
            line.strip()
            for line in COMMENTS_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    
    return [
        "Started working on this.",
        "This is ready for review.",
        "Blocked at the moment, will update."
    ]

COMMENT_TEMPLATES = load_comment_templates()
