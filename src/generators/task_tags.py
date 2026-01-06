import random

def generate_task_tags(conn, tasks, tags):
    cursor = conn.cursor()

    for task in tasks:
        task_id = task["task_id"]

        # Tagging is intentionally inconsistent to reflect real-world usage
        if random.random() < 0.4:
            continue

        num_tags = random.randint(1, 3)
        selected_tags = random.sample(tags, min(num_tags, len(tags)))

        for tag in selected_tags:
            cursor.execute(
                """
                INSERT INTO task_tags (task_id, tag_id)
                VALUES (?, ?)
                """,
                (task_id, tag["tag_id"])
            )

    conn.commit()
