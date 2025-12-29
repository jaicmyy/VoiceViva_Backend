import secrets
import string
from werkzeug.security import generate_password_hash


def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_password_and_hash():
    plain_password = generate_random_password()
    hashed_password = generate_password_hash(plain_password)
    return plain_password, hashed_password
