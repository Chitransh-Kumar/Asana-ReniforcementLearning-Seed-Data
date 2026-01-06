import random

def generate_custom_field_values(conn, tasks, field_defs):
    cursor = conn.cursor()

    # Group custom fields by project to enforce project-scoped metadata
    project_fields = {}
    for f in field_defs:
        project_fields.setdefault(f["project_id"], []).append(f)

    for task in tasks:
        task_id = task["task_id"]
        project_id = task["project_id"]

        fields = project_fields.get(project_id, [])
        if not fields:
            continue

        for field in fields:
            # Custom fields are intentionally sparse, not every task is fully populated
            if random.random() < 0.4:
                continue

            field_id = field["field_id"]
            field_type = field["field_type"]

            if field_type == "enum":
                value = random.choice(field["enum_values"])
            elif field_type == "number":
                value = str(random.randint(1, 13))
            elif field_type == "text":
                value = random.choice([
                    "Needs follow-up",
                    "Aligned with plan",
                    "Pending review",
                    "No additional notes"
                ])
            else:
                value = None

            cursor.execute(
                """
                INSERT INTO custom_field_values
                (field_id, task_id, value)
                VALUES (?, ?, ?)
                """,
                (field_id, task_id, value)
            )

    conn.commit()
