from lib.security import check_password_hash, generate_password_hash


async def generate_password(password):
    password_hash = generate_password_hash(password)
    return password_hash


async def check_password(password_hash, password):
    return check_password_hash(password_hash, password)
