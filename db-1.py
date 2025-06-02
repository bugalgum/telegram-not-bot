import sqlite3

# РЎРѕР·РґР°РЅРёРµ С‚Р°Р±Р»РёС†С‹ РїСЂРё РїРµСЂРІРѕРј Р·Р°РїСѓСЃРєРµ
def init_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_note(user_id: int, text: str):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()
    conn.close()

def get_notes(user_id: int):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT text FROM notes WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]
    
def delete_note_by_index(user_id: int, index: int):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT id FROM notes WHERE user_id = ?", (user_id,))
    all_ids = [row[0] for row in c.fetchall()]
    if 0 <= index < len(all_ids):
        note_id = all_ids[index]
        c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def clear_notes(user_id: int):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()