# Password Manager

A secure web-based Password Manager built with Python, Flask, SQLite, and the Fernet encryption library. The application allows authenticated users to securely store, manage, import, and export passwords.

---

## Features

- User registration and login
- Secure password hashing using Werkzeug
- Password encryption using Fernet
- Add new passwords
- Edit existing passwords
- Delete passwords
- Search passwords by website or username
- Password generator
- Password strength indicator
- Show/Hide password
- Copy password to clipboard
- Import passwords from CSV
- Export passwords to CSV
- User-specific password storage
- Bootstrap responsive interface

---

## Technologies Used

- Python 3
- Flask
- SQLite
- Flask-Login
- Cryptography (Fernet)
- Bootstrap 5
- HTML5
- CSS3
- JavaScript

---

## Project Structure

```
password-manager/
│
├── app.py
├── admin.py
├── crypto.py
├── utils.py
├── generate_key.py
├── requirements.txt
├── README.md
├── .gitignore
├── .secret.key (ignored by Git)
│
├── database/
│   └── passwords.db
│
├── models/
│   ├── database.py
│   └── user.py
│
├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_password.html
│   ├── edit_password.html
│   └── import_passwords.html
│
└── static/
    └── css/
        └── style.css
```

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/TaBongs/password-manager.git
```

2. Navigate into the project

```bash
cd password-manager
```

3. Create a virtual environment

```bash
python -m venv .venv
```

4. Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Generate the encryption key

```bash
python generate_key.py
```

7. Create the database

```bash
python models/database.py
```

8. Create the admin account

```bash
python admin.py
```

9. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Security Features

- Passwords are encrypted using Fernet encryption.
- User passwords are hashed using Werkzeug.
- Each user can only access their own stored passwords.
- Encryption keys are stored outside version control.
- Sensitive files are ignored using `.gitignore`.

---

## Future Improvements

- Password categories
- Two-factor authentication (2FA)
- Password expiry reminders
- Secure password sharing
- Cloud database support
- Dark mode
- Mobile responsive improvements

---

## Author

Bongani Phiri
Information Systems & Cyber Security Student