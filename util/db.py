import sqlite3
DB_FILE="data/stat.db"

def createTable():
    """Creates the two main data tables for users and list of stories."""
    db = sqlite3.connect("../"+DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE stat (username TEXT, display TEXT, age INTEGER, best_score INTEGER)"
    c.execute(command)

    command = "CREATE TABLE game (username TEXT, money INTEGER, hp INTEGER, fun INTEGER, experience INTEGER, hours INTEGER)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

# createTable()

def add_user(username, password):
    """Insert credentials for newly registered user into database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    """Authenticate a user attempting to log in."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # user_info = c.execute("SELECT users.username, users.password FROM users WHERE username={} AND password={}".format(username, password))
    for entry in c.execute("SELECT users.username, users.password FROM users"):
        if(entry[0] == username and entry[1] == password):
            db.close()
            return True
    db.close()
    return False

def check_user(username):
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            db.close()
            return True
    db.close()
    return False

def get_profile(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    result = []
    try:
        profile = c.execute("SELECT display, age, best_score FROM stat WHERE username = '{}'".format(username)).fetchone()
        # print(profile)
        for i in range(3):
            if (i==2 and profile[i]==-1):
                result.append("N/A")
            else:
                result.append(profile[i])
    except:
        for i in range(3):
            result.append("N/A")
    return result

def edit_profile(username, display_name, age):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    score = -1
    try:
        score = c.execute("SELECT best_score FROM stat WHERE username='{}'".format(username)).fetchone()[0]
        c.execute("DELETE FROM stat WHERE username = '{}'".format(username))
    except:
        pass
    c.execute("INSERT INTO stat VALUES(?, ?, ?, ?)", (username, display_name, age, score))

    db.commit()
    db.close()
