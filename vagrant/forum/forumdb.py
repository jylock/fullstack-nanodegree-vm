#
# Database access functions for the web forum.
#

import psycopg2
import bleach


# Get posts from database.
def get_all_posts():
    db = psycopg2.connect("dbname=forum")
    cur = db.cursor()

    cur.execute("SELECT time, content FROM posts ORDER BY time DESC")
    posts = ({'content': str(row[1]), 'time': str(row[0])} for row in cur.fetchall())

    db.close()
    return posts


# Add a post to the database.
def add_post(content):
    db = psycopg2.connect("dbname=forum")
    cur = db.cursor()

    cur.execute("INSERT INTO posts (content) VALUES (%s)", (bleach.clean(content, strip=True),))
    db.commit()
    db.close()