from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    Response
)
import csv
import io

from utils import generate_password

from datetime import datetime

from models.database import get_connection

from crypto import (

    encrypt_password,

    decrypt_password

)

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user import (
    get_user_by_id,
    get_user_by_username
)

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):

    return get_user_by_id(user_id)

@app.route("/")
@login_required
def dashboard():

    conn = get_connection()

    search = request.args.get("search", "").strip()

    if search:

        passwords = conn.execute(
            """
            SELECT *
            FROM passwords
            WHERE user_id = ?
            AND (
                website LIKE ?
                OR username LIKE ?
            )
            ORDER BY id DESC
            """,
            (
                current_user.id,
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    else:

        passwords = conn.execute(
            """
            SELECT *
            FROM passwords
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (
                current_user.id,
            )
        ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        passwords=passwords,
        decrypt_password=decrypt_password
    )

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_password():

    if request.method == "POST":

        website = request.form["website"]

        username = request.form["username"]

        encrypted_password = encrypt_password(
            request.form["password"]
        )

        notes = request.form.get(
            "notes",
            ""
        )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        conn = get_connection()

        conn.execute(

            """

            INSERT INTO passwords

            (

                user_id,

                website,

                username,

                encrypted_password,

                notes,

                created_at,

                updated_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

            """,

            (

                current_user.id,

                website,

                username,

                encrypted_password,

                notes,

                now,

                now

            )

        )

        conn.commit()

        conn.close()

        flash(
            "Password added successfully.",
            "success"
        )

        return redirect("/")

    return render_template("add_password.html")

@app.route("/edit/<int:password_id>", methods=["GET", "POST"])
@login_required
def edit_password(password_id):

    conn = get_connection()

    if request.method == "POST":

        website = request.form["website"]

        username = request.form["username"]

        encrypted_password = encrypt_password(
            request.form["password"]
        )

        notes = request.form.get(
            "notes",
            ""
        )

        updated_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        conn.execute(

            """

            UPDATE passwords

            SET

                website=?,

                username=?,

                encrypted_password=?,

                notes=?,

                updated_at=?

            WHERE id=?

            AND user_id=?

            """,

            (

                website,

                username,

                encrypted_password,

                notes,

                updated_at,

                password_id,

                current_user.id

            )

        )

        conn.commit()

        conn.close()

        flash(
            "Password updated successfully.",
            "success"
        )

        return redirect("/")

    password = conn.execute(

        """

        SELECT *

        FROM passwords

        WHERE id=?

        AND user_id=?

        """,

        (

            password_id,

            current_user.id

        )

    ).fetchone()

    if password is None:

        conn.close()

        flash(
            "Password not found.",
            "danger"
        )

        return redirect("/")

    conn.close()

    return render_template(

        "edit_password.html",

        password=password,

        decrypt_password=decrypt_password

    )

@app.route("/delete/<int:password_id>")
@login_required
def delete_password(password_id):

    conn = get_connection()

    result = conn.execute(

        """

        DELETE FROM passwords

        WHERE id = ?

        AND user_id = ?

        """,

        (

            password_id,

            current_user.id

        )

    )

    conn.commit()

    if result.rowcount == 0:

        flash(
            "Password not found.",
            "danger"
        )

    else:

        flash(
            "Password deleted successfully.",
            "success"
        )

    conn.close()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = get_user_by_username(username)

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect("/")

        flash(
            "Invalid username or password.",
            "danger"
        )

        return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")

@app.route("/generate-password")
@login_required
def generate_random_password():

    password = generate_password()

    return {
        "password": password
    }

@app.route("/export")
@login_required
def export_passwords():

    conn = get_connection()

    passwords = conn.execute(
        """
        SELECT *
        FROM passwords
        WHERE user_id = ?
        ORDER BY website
        """,
        (
            current_user.id,
        )
    ).fetchall()

    conn.close()

    def generate():

        yield "Website,Username,Password,Notes,Created,Updated\n"

        for password in passwords:

            decrypted = decrypt_password(
                password["encrypted_password"]
            )

            yield (
                f'"{password["website"]}",'
                f'"{password["username"]}",'
                f'"{decrypted}",'
                f'"{password["notes"]}",'
                f'"{password["created_at"]}",'
                f'"{password["updated_at"]}"\n'
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=passwords.csv"
        }
    )
    
@app.route("/import", methods=["GET", "POST"])
@login_required
def import_passwords():

    if request.method == "POST":

        file = request.files.get("csv_file")

        if not file:

            flash(
                "Please select a CSV file.",
                "danger"
            )

            return redirect("/import")

        try:

            import io
            import csv

            stream = io.StringIO(
                file.stream.read().decode("UTF-8"),
                newline=None
            )

            reader = csv.DictReader(stream)

            conn = get_connection()

            now = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            count = 0

            for row in reader:

                encrypted_password = encrypt_password(
                    row["Password"]
                )

                conn.execute(

                    """

                    INSERT INTO passwords

                    (

                        user_id,

                        website,

                        username,

                        encrypted_password,

                        notes,

                        created_at,

                        updated_at

                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?)

                    """,

                    (

                        current_user.id,

                        row["Website"],

                        row["Username"],

                        encrypted_password,

                        row.get("Notes", ""),

                        now,

                        now

                    )

                )

                count += 1

            conn.commit()

            conn.close()

            flash(
                f"{count} passwords imported successfully.",
                "success"
            )

            return redirect("/")

        except Exception as e:

            flash(
                f"Import failed: {e}",
                "danger"
            )

            return redirect("/import")

    return render_template("import_passwords.html")
        
if __name__ == "__main__":

    app.run(debug=True)