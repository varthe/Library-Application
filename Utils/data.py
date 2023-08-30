import re, bcrypt

"""
A collection of useful functions used throughout the application
Includes validation and encryption
"""
def validateEmail(email):
    """
    Checks if the provided email is not empty
    :param email: Email
    :return: True if the email is not empty, False if it is empty
    """
    if len(email) > 0:
        return True
    return False
def validateName(name):
    """
    Checks if the provided name only contains letters
    :param name: Name
    :return: True if the name only contains letters, False if it contains any other characters
    """
    if name.isalpha():
        return True
    return False

def validatePassword(password):
    """
    Check if there is a special character in the password and if the length of the password is between 8 and 2 characters
    :param password: Password
    :return: True if the password matches the conditions, False if it doesn't
    """
    if re.search("[^a-zA-Z0-9s]", password) and 8 < len(password) < 20:
        return True
    return False

def hashPassword(password):
    """
    Hashes the password to be stored in the database
    :param password: Original password
    :return: Hashed password
    """
    password = password.encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
    return hashed

def comparePasswords(password, hashed):
    """
    Checks if the password matches to the hashed password in the database
    :param password: Password
    :param hashed: Hashed password
    :return: True if the passwords match, False if they don't
    """
    password = password.encode("utf-8")
    if bcrypt.checkpw(password, hashed):
        return True
    return False

