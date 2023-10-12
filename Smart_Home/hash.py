import bcrypt

def hash_password(password):
    # Generate a salt and hash a password
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')  # Encode the password to bytes
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password

def check_password(input_password, db_pass):
    # Encode the input password and hashed password to bytes
    input_password_bytes = input_password.encode('utf-8')
    db_pass_bytes = db_pass.encode('utf-8')

    # Check if the input password matches the hashed password
    if bcrypt.checkpw(input_password_bytes, db_pass_bytes):
        print("Password matches the hashed password.")
        return True
    else:
        print("Password does not match the hashed password.")
        return False

