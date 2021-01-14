# https://pythonise.com/categories/python/python-password-hashing-bcrypt
import bcrypt


# passowrd given by the user to put into the database
def hash_password(password):
    # encode the password so we dont need to in the main application.
    password = password.encode('utf-8')
    # dencode the hashed password since we won't store it encoded.
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
    return hashed


# password is the password the user is using to login
# hashed should be the saved hash in the database
def check_password(password, hashed):
    # encode the password so we dont need to in the main application.
    password = password.encode('utf-8')
    # encode the hashed password from the database since we won't store it encoded.
    hashed = hashed.encode('utf-8')
    # retrun true/false
    return bcrypt.checkpw(password, hashed)
