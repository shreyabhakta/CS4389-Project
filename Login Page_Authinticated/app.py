from flask import Flask, render_template, send_from_directory, request, redirect, url_for, make_response
import string
import random

app = Flask(__name__, template_folder="./", static_folder="./src")


USERS_STORED = []

@app.route("/src/<path:path>")
def file_access(path):
    print("here")
    return send_from_directory("./src", path)


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        pass
    elif request.method == "POST":
        print("Data sent by the user to login")
        password, email = None, None
        try:
            login_data = request.json
            password = login_data.get("password", None)
            email = login_data.get("email", None)
        except Exception as identifier:
            print("Invalid data sent by the user")

        if email and password:
            print(email, password)
            response = make_response(redirect(url_for("dashboard")), 302)
            session_id = get_random_string(10)
            print("session", session_id)
            USERS_STORED.append(session_id)
            response.set_cookie("rrrr", session_id)
            return response

    return "Invalid Login Credentials"


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@app.route("/dashboard")
def dashboard():
    current_session = request.cookies.get("rrrr")
    if current_session:
        for session in USERS_STORED:
            if current_session == session:
                return render_template("bankUser.html")

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
