from werkzeug.security import generate_password_hash

from models.database import get_connection


def create_admin():

    conn = get_connection()

    username = "admin"

    password = generate_password_hash("admin123")

    full_name = "Administrator"

    existing = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    if existing:

        print("Admin already exists.")

    else:

        conn.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                full_name
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                password,
                full_name
            )
        )

        conn.commit()

        print("Admin user created successfully.")

    conn.close()


if __name__ == "__main__":

    create_admin()