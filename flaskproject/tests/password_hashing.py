from modules.password_hashing import hash_password, check_password


def correct():
    password = 'P@ssW0rd!'
    hashed = hash_password(password)
    check = check_password(password, hashed)
    # print('Password: ' + str(password) +
    #      '\nHashed password: ' + str(hashed) +
    #      '\nCheck: ' + str(check))
    if check == True:
        result = 'Passed correct password hashing check.'
    else:
        result = 'Failed correct password hashing check.'
    print(result)


def incorrect():
    password = 'P@ssW0rd!'
    hashed = hash_password(password)
    check = check_password('P@ssW0rd!zyx', hashed)
    # print('Password: ' + str(password) +
    #      '\nHashed password: ' + str(hashed) +
    #      '\nCheck: ' + str(check))
    if check == False:
        result = 'Passed incorrect password hashing check.'
    else:
        result = 'Failed incorrect password hashing check.'
    print(result)
