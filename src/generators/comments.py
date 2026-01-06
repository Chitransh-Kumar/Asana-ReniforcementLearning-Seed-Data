import random
from datetime import datetime, timezone

from utils.uuid import generate_uuid
from utils.dates import random_past_datetime
from constants.comment_templates import COMMENT_TEMPLATES
from config.settings import MAX_COMMENTS_PER_TASK

def generate_comments(conn, tasks, team_memberships):
    cursor = conn.cursor()
    comments = []

    # Pre-group users by team to ensure comments come from valid collaborators
    team_users = {}
    for tm in team_memberships:
        team_users.setdefault(tm["team_id"], []).append(tm["user_id"])

    for task in tasks:
        # Not all tasks have discussion activity
        if random.random() < 0.6:
            continue

        task_id = task["task_id"]

        cursor.execute(
            """
            SELECT project_id, created_at, completed_at
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,)
        )
        task_row = cursor.fetchone()
        if not task_row:
            continue

        cursor.execute(
            """
            SELECT team_id
            FROM projects
            WHERE project_id = ?
            """,
            (task_row["project_id"],)
        )
        project_row = cursor.fetchone()
        if not project_row:
            continue

        # Comment authors restricted to members of the owning team
        possible_authors = team_users.get(project_row["team_id"], [])
        if not possible_authors:
            continue

        num_comments = random.randint(1, MAX_COMMENTS_PER_TASK)

        for _ in range(num_comments):
            comment_id = generate_uuid()
            author_id = random.choice(possible_authors)
            content = random.choice(COMMENT_TEMPLATES)

            start_time = datetime.fromisoformat(task_row["created_at"])
            if task_row["completed_at"]:
                end_time = datetime.fromisoformat(task_row["completed_at"])
            else:
                end_time = datetime.now(timezone.utc)

            # Comment timestamps constrained to the task lifecycle
            created_at = random_past_datetime(0, 90)
            if created_at < start_time:
                created_at = start_time
            if created_at > end_time:
                created_at = end_time

            cursor.execute(
                """
                INSERT INTO comments
                (comment_id, task_id, author_id, content, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    comment_id,
                    task_id,
                    author_id,
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
