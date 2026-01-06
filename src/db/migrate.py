from pathlib import Path

def run_migrations(conn, schema_path= "schema.sql"):
    # Applies full schema in a single transaction to initialize the database
    schema_file = Path(schema_path)

    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
