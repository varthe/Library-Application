import sqlite3, datetime
from Utils import data
import tkinter.messagebox

def loginUser(email, password):
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    if userExists(c, email):
        c.execute("SELECT * FROM users WHERE email = ? LIMIT 1", [email])
        userInfo = c.fetchall()
        hashedPassword = userInfo[0][4]
        conn.close()

        if data.comparePasswords(password, hashedPassword):
            return {"userID": userInfo[0][0], "email": email, "firstName": userInfo[0][2], "lastName": userInfo[0][3]}
    return False


def userExists(c, email):
    user = c.execute("SELECT userID FROM users WHERE email = ? LIMIT 1", [email]).fetchall()
    if len(user) > 0:
        return True
    else:
        return False

def createUser(email, password, firstName, lastName):
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    if not userExists(c, email):
        c.execute("INSERT INTO users (email, firstName, lastName, password) VALUES (?, ?, ?, ?)", [email, firstName, lastName, password])
        conn.commit()
        conn.close()
        return True
    return False

def listAllBooks():
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    result = c.fetchall()
    conn.close()
    return result

def listAvailableBooks():
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE available = 1")
    result = c.fetchall()
    conn.close()
    return result

def listBooksDueToday():
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    dateToday = datetime.datetime.now().strftime("%d/%m/%y")
    c.execute("SELECT * FROM books WHERE dueDate = ?", [dateToday])
    result = c.fetchall()
    return result

def listUnavailableBooks():
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE available = 0")
    result = c.fetchall()
    return result
def borrowBook(book, user, dueDate):
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    c.execute("UPDATE books SET available = 0, dueDate = ?, userID = ? WHERE bookID = ?", [dueDate, user.userID, book.bookID])
    conn.commit()
    conn.close()

def getBorrowerInfo(book):
    conn = sqlite3.connect("LibraryApplication.db")
    c = conn.cursor()
    c.execute("SELECT email, firstName, lastName FROM users WHERE userID = ? LIMIT 1", [book.userID])
    result = c.fetchall()
    conn.close()
    if(len(result) > 0):
        return {"email": result[0][0], "firstName": result[0][1], "lastName": result[0][2]}

