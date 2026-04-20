import bcrypt

def get_hash_password(password:str):
    hash_pwd=bcrypt.hashpw(password=password.encode(),salt=bcrypt.gensalt(10))
    return hash_pwd.decode()

def verify_password(plain_password:str,hashed_password:str):
    return bcrypt.checkpw(password=plain_password.encode(),hashed_password=hashed_password.encode())