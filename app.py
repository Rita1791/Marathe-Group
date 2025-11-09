import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host=st.secrets["PG_HOST"],
    dbname=st.secrets["PG_DB"],
    user=st.secrets["PG_USER"],
    password=st.secrets["PG_PASS"],
    port=st.secrets.get("PG_PORT", 5432)
)

def fetch_customers():
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM customers ORDER BY created_at DESC")
        return cur.fetchall()
