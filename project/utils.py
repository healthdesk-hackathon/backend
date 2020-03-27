import secrets


def generate_secret(size=64):
    return secrets.token_hex(size)
