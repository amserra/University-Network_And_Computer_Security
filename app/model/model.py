from app.model.db import get_db

### ALWAYS use prepared statements

def db_get_user_by_id(user_id):
    return get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

def db_get_user_by_email(email):
    return get_db().execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

def db_create_user(name, email, hashed_password):
    db = get_db()
    try:
        db.execute("INSERT INTO user (name, email, password) VALUES (?, ?, ?)",(name, email, hashed_password),)
    except:
        return
    db.commit()
