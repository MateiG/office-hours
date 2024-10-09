from flask import session


def clear_session():
    session.pop("auth", None)
    session.pop("user", None)
