import secrets
import string


def get_password() -> str:
    length = 20
    pwd = ''
    alphabet = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd
