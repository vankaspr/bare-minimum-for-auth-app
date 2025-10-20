import bcrypt

def hash_password(pwd: str) -> str:
    """Password hashing with salt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(
        password=pwd.encode("utf-8"), 
        salt=salt
    )
    return hashed.decode("utf-8")

def verify_password(
    pwd: str,
    hashed_pwd: str,
) -> bool:
    """Password checking"""
    return bcrypt.checkpw(
        password=pwd.encode("utf-8"),
        hashed_password=hashed_pwd.encode("utf-8")
    )