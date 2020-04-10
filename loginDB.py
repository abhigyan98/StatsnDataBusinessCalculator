import sqlite3

con = sqlite3.connect('employee.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS user(
            email VARCHAR2(500) PRIMARY KEY,
            name VARCHAR2(500) NOT NULL,
            password VARCHAR2(100) NOT NULL,
            image VARCHAR2(150) DEFAULT 'img_avatar.png'
        )
    """)

def createUser(email,name,password,image):
    db.execute("INSERT INTO user VALUES (?,?,?,?)",(email,name,password,image))
    con.commit()

def getPasswordForLogin(email):
    db.execute("SELECT password FROM user WHERE email=(?)",(email,))
    password = db.fetchall()
    return password

def userImage(email):
    db.execute("SELECT image FROM user WHERE email=(?)",(email,))
    image = db.fetchall()
    return image

def getUser(email):
    db.execute("SELECT * FROM user WHERE email=(?)",(email,))
    user = db.fetchall()
    return user

#createTable()