
from mysql.connector import Error
from logger import log
from Nerves import create_connection_route

def save_memory(text):
    try:
        conn = create_connection_route()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO memories (text) VALUES (%s)",
            (text,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Error as e:
        log(f"STOMACH | save FAILED: {e}")
        return False


def get_memories(keyword="", limit=10):
    try:
        conn = create_connection_route()
        cur = conn.cursor()
        cur.execute(
            "SELECT text FROM memories WHERE text LIKE %s ORDER BY id DESC LIMIT %s",
            (f"%{keyword}%", limit)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [row[0] for row in rows]

    except Error as e:
        log(f"STOMACH | read FAILED: {e}")
        return []
