import libsql
import os

url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")

conn_local = libsql.connect('static/sources.db')
cur_local = conn_local.cursor()


conn = libsql.connect('sources.db', sync_url=url, auth_token=auth_token)
cursor = conn.cursor()

table = "TAGS_FURTHER"

'''cursor.execute(f"""
CREATE TABLE "{table}" (
	"ID"	INTEGER,
	"TAG_ID"	INTEGER,
	"FURT_ID"	INTEGER,
	PRIMARY KEY("ID"),
    FOREIGN KEY ("FURT_ID") REFERENCES FURTHER("ID"),
    FOREIGN KEY ("TAG_ID") REFERENCES TAGS("ID")
)
""")'''

for row in cur_local.execute(f"SELECT * FROM {table}").fetchall():
    cursor.execute(
        f"INSERT INTO {table} (id, tag_id, furt_id) VALUES (?, ?, ?)",
        (row[0], row[1], row[2])
    )
conn.commit()
conn.sync()