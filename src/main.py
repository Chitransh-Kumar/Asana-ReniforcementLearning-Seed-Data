import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import os
from db.connection import get_connection
from db.migrate import run_migrations
from generators.organizations import generate_organization
from config.settings import DB_PATH
from generators.teams import generate_teams
from generators.users import generate_users
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.subtasks import generate_subtasks
from generators.comments import generate_comments
from generators.tags import generate_tags
from generators.task_tags import generate_task_tags
from generators.custom_field_definitions import generate_custom_field_definitions
from generators.custom_field_values import generate_custom_field_values


def main():
    # Idempotent entrypoint: regenerate the full workspace from scratch
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection(DB_PATH)
    run_migrations(conn)

    # Organization -> teams -> users form the structural backbone
    org = generate_organization(conn)

    teams = generate_teams(conn, org["org_id"])
    print(f"Generated {len(teams)} teams")

    users = generate_users(conn, org["org_id"], org["domain"])
    print(f"Generated {len(users)} users")

    team_memberships = generate_team_memberships(conn, users, teams)
    print("Team memberships generated")

    # # Projects and sections define workflow context
    projects = generate_projects(conn, teams)
    print(f"Generated {len(projects)} projects")

    sections = generate_sections(conn, projects)
    print(f"Generated {len(sections)} sections")

    # # Tasks and subtasks capture execution-level behavior
    tasks = generate_tasks(conn, projects, sections, team_memberships)
    print(f"Generated {len(tasks)} tasks")

    subtasks = generate_subtasks(conn, tasks)
    print(f"Generated {len(subtasks)} subtasks")

    # # Collaboration and metadata layers
    comments = generate_comments(conn, tasks)
    print(f"Generated {len(comments)} comments")

    tags = generate_tags(conn)
    generate_task_tags(conn, tasks, tags)
    print("Tags assigned to tasks")

    field_defs = generate_custom_field_definitions(conn, projects)
    generate_custom_field_values(conn, tasks, field_defs)
    print("Custom fields populated")

    conn.close()
    print("Database initialized with organization:", org["org_id"])

if __name__ == "__main__":
    main()
