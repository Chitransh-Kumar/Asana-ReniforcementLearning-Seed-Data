from utils.uuid import generate_uuid
from constants.tag_vocab import TAG_VOCAB

def generate_tags(conn):
    cursor = conn.cursor()
    tags = []

    # Tags are global and created once, then reused across all projects and tasks
    for name in TAG_VOCAB:
        tag_id = generate_uuid()

        cursor.execute(
            """
            INSERT INTO tags (tag_id, name)
            VALUES (?, ?)
            """,
            (tag_id, name)
        )

        tags.append({
            "tag_id": tag_id,
            "name": name
        })

    conn.commit()
    return tags
