import random
from datetime import datetime, timedelta, timezone

from utils.uuid import generate_uuid
from constants.comment_templates import COMMENT_TEMPLATES
from config.settings import MAX_COMMENTS_PER_TASK


def generate_comments(conn, tasks):
    cursor = conn.cursor()
    comments = []

    now = datetime.now()

    for task in tasks:
        # Not all tasks have comments
        if random.random() < 0.6:
            continue

        task_id = task["task_id"]

        cursor.execute(
            """
            SELECT assignee_id, created_at, completed_at
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,)
        )
        row = cursor.fetchone()
        if not row:
            continue

        assignee_id, task_created_at, task_completed_at = row

        # Author must be task assignee
        if assignee_id is None:
            continue

        start_time = datetime.fromisoformat(task_created_at)
        end_time = (
            datetime.fromisoformat(task_completed_at)
            if task_completed_at
            else now
        )

        num_comments = random.randint(1, MAX_COMMENTS_PER_TASK)

        for _ in range(num_comments):
            comment_id = generate_uuid()
            content = random.choice(COMMENT_TEMPLATES)

            # Sample timestamp within task lifecycle
            delta_seconds = int((end_time - start_time).total_seconds())
            if delta_seconds <= 0:
                created_at = start_time
            else:
                created_at = start_time + timedelta(
                    seconds=random.randint(0, delta_seconds)
                )

            cursor.execute(
                """
                INSERT INTO comments
                (comment_id, task_id, author_id, content, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    comment_id,
                    task_id,
                    assignee_id,
                    content,
                    created_at.isoformat()
                )
            )

            comments.append({
                "comment_id": comment_id,
                "task_id": task_id
            })

    conn.commit()
    return comments
