from utils.uuid import generate_uuid
from utils.dates import random_past_datetime
from config.settings import ORG_MIN_AGE_YEARS, ORG_MAX_AGE_YEARS

def generate_organization(conn):
    org_id = generate_uuid()

    # Single fixed organization to model a mature, long-lived enterprise workspace
    name = "Zapier"
    domain = "zapier.com"

    created_at = random_past_datetime(
        min_days_ago=ORG_MIN_AGE_YEARS * 365,
        max_days_ago=ORG_MAX_AGE_YEARS * 365
    )

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO organizations (org_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (org_id, name, domain, created_at.isoformat())
    )

    conn.commit()

    return {
        "org_id": org_id,
        "domain": domain
    }
