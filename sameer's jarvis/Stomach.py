from Nerves import create_connection_route
from Mouth import speak
from Hand import APPS, SITES


def memorize_app(name, path):
    name = name.lower()
    db = create_connection_route()
    cursor = db.cursor()
    cursor.execute("REPLACE INTO memorized_apps (name, path) VALUES (%s, %s)", (name, path))
    db.commit()
    db.close()
    APPS[name] = path
    speak("I have memorized " + name)


def memorize_website(name, url):
    name = name.lower().replace(" ", "").replace("site", "")
    db = create_connection_route()
    cursor = db.cursor()
    cursor.execute("REPLACE INTO memorized_websites (name, url) VALUES (%s, %s)", (name, url))
    db.commit()
    db.close()
    SITES[name] = url
    speak("I have memorized " + name)


def memorize_text(text):
    db = create_connection_route()
    cursor = db.cursor()
    cursor.execute("INSERT INTO memorized_text (text) VALUES (%s)", (text,))
    db.commit()
    db.close()
    speak("I have memorized that")


def show_memorized_apps():
    db = create_connection_route()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM memorized_apps")
    rows = cursor.fetchall()
    db.close()
    if rows:
        for row in rows:
            speak(row[0])
    else:
        speak("No apps saved yet")


def show_memorized_websites():
    db = create_connection_route()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM memorized_websites")
    rows = cursor.fetchall()
    db.close()
    if rows:
        for row in rows:
            speak(row[0])
    else:
        speak("No websites saved yet")


def show_memorized_texts():
    db = create_connection_route()
    cursor = db.cursor()
    cursor.execute("SELECT text FROM memorized_text ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    db.close()
    if rows:
        for row in rows:
            speak(row[0])
    else:
        speak("No notes saved yet")


def load_memorized():
    # Runs once when Jarvis starts. Puts saved apps and websites back into the lists.
    db = create_connection_route()
    cursor = db.cursor()

    cursor.execute("SELECT name, path FROM memorized_apps")
    for name, path in cursor.fetchall():
        APPS[name] = path

    cursor.execute("SELECT name, url FROM memorized_websites")
    for name, url in cursor.fetchall():
        SITES[name] = url

    db.close()