from flask_login import current_user


def get_credentials():
    return current_user.credentials
