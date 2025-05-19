import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="resume_matcher",
        user="postgres",
        password="postgres"
    )
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY, 
                category TEXT,
                data JSONB
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jds (
                jd_id TEXT PRIMARY KEY,  
                company TEXT,
                category TEXT,
                data JSONB
            )
        """)
