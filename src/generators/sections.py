from utils.uuid import generate_uuid
from constants.workflows import PROJECT_WORKFLOWS

def generate_sections(conn, projects):
    cursor = conn.cursor()
    sections = []

    for project in projects:
        project_id = project["project_id"]
        project_type = project["project_type"]

        # Sections are generated from project-type–specific workflows
        workflow = PROJECT_WORKFLOWS[project_type]

        for position, name in enumerate(workflow, start=1):
            section_id = generate_uuid()

            cursor.execute(
                """
                INSERT INTO sections (section_id, project_id, name, position)
                VALUES (?, ?, ?, ?)
                """,
                (section_id, project_id, name, position)
            )

            sections.append({
                "section_id": section_id,
                "project_id": project_id
            })

    conn.commit()
    return sections
