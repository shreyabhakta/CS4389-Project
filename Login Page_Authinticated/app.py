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

            # Check if the user,password is valid in DB

            # Generate a random 5 digit variable here
            CODE = 12345

            # Update DB of this email to store the code

            # Send an email to the user with the code
            import smtplib
            from email.message import EmailMessage
            from email.mime.text import MIMEText

            GMAIL_USER = "exampleuserjane@gmail.com"
            GMAIL_PASS = "Merlot123"
            EMAIL_BODY = """Your code is {}.""".format(CODE)
            print(EMAIL_BODY)
            # Now send the EMail
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(GMAIL_USER, GMAIL_PASS)
                server.sendmail(GMAIL_USER, email, EMAIL_BODY)
                server.close()
                print("EMAIL SENT")
            except Exception as e:
                print(e)
                print('Something went wrong..., cannot send email')

            response = make_response(
                redirect(url_for("two_factor", email=email)), 302)
            # session_id = get_random_string(10)
            # print("session", session_id)
            # USERS_STORED.append(session_id)
            # response.set_cookie("rrrr", session_id)
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


@app.route("/twofactor", methods=['GET', 'POST'])
def two_factor():

    if request.method == "GET":
        email = request.args.get("email", None)
        if not email:
            return "Invalid URL"
        return render_template('two_factor.html', email=email)
    elif request.method == "POST":
        print(request.form)
        email = request.form.get("email", None)
        code = request.form.get("code", None)

        # Check if the code matches in the DB for the given email

        # If not return error page

        # Else return dashbord
        if email and code:
            print(email, code)
            response = make_response(
                redirect(url_for("dashboard")), 302)
            session_id = get_random_string(10)
            print("session", session_id)
            USERS_STORED.append(session_id)
            response.set_cookie("rrrr", session_id)
            return response

        return "HELLOO"


if __name__ == '__main__':
    app.run(debug=True)
