from flask_login import UserMixin

from models.database import get_connection


class User(UserMixin):

    def __init__(
        self,
        id,
        username,
        password,
        full_name
    ):

        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name


def get_user_by_id(user_id):

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    if user:

        return User(
            user["id"],
            user["username"],
            user["password"],
            user["full_name"]
        )

    return None


def get_user_by_username(username):

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    conn.close()

    if user:

        return User(
            user["id"],
            user["username"],
            user["password"],
            user["full_name"]
        )

    return None