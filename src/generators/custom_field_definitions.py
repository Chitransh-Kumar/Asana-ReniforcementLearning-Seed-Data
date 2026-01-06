from utils.uuid import generate_uuid
from constants.custom_fields import CUSTOM_FIELD_TEMPLATES

def generate_custom_field_definitions(conn, projects):
    cursor = conn.cursor()
    field_defs = []

    for project in projects:
        project_id = project["project_id"]
        project_type = project["project_type"]

        # Custom fields are scoped per project to mirror Asana’s customization model
        templates = CUSTOM_FIELD_TEMPLATES.get(project_type, [])

        for name, field_type, enum_values in templates:
            field_id = generate_uuid()

            cursor.execute(
                """
                INSERT INTO custom_field_definitions
                (field_id, project_id, name, field_type)
                VALUES (?, ?, ?, ?)
                """,
                (field_id, project_id, name, field_type)
            )

            field_defs.append({
                "field_id": field_id,
                "project_id": project_id,
                "field_type": field_type,
                "enum_values": enum_values
            })

    conn.commit()
    return field_defs
