
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, make_response
from flaskext.mysql import MySQL
from random import sample as SAMPLE, choice as CHOICE
from string import digits as DIGITS, ascii_lowercase as LOWERCASE
from config import config_development as DEV

app = Flask(
    __name__, template_folder=DEV.TEMPLATES_FOLDER, static_folder=DEV.STATIC_FOLDER
)
app.config.from_object(DEV)


mysql = MySQL()
mysql.init_app(app=app)


USERS_STORED = []


@app.route("/src/<path:path>")
def file_access(path):
    print("here")
    return send_from_directory("./src", path)


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/createaccount", methods=['POST'])
def create_account():

    def query_db(query, is_update=False):
        connection = mysql.connect()
        cursor = connection.cursor()
        res = []
        try:
            cursor.execute(query=query)
            if is_update:
                connection.commit()
            else:
                res = cursor.fetchall()
        except Exception as identifier:
            print(identifier)
        finally:
            cursor.close()
            connection.close()
        return res if not is_update else None

    password, email = None, None
    first_name, last_name = None, None
    phone_number, ssn = None, None
    try:
        login_data = request.json
        password = login_data.get("password", None)
        email = login_data.get("email", None)
        first_name = login_data.get("first", None)
        last_name = login_data.get("last", None)
        phone_number = login_data.get("phone", None)
        if len(phone_number) > 15:
            return "Invalid phone number"
        ssn = login_data.get("ssn", None)
        if len(ssn) != 4:
            return "Invalid SSN legth"
    except Exception as identifier:
        print(identifier)
        print("Invalid data sent by the user")
        return("INVALID data sent!")

    # Form is missing data
    if not (email and password and first_name and last_name and phone_number and ssn):
        return "Missing fields!!"

    # QUery to check if a user already there
    if len(query_db("SELECT * FROM user where first_name = '{}' and last_name= '{}' and ssn = {}  ".format(first_name, last_name, ssn))) > 0:
        return "User {}, {} has an account with us".format(last_name, first_name)

    # New user found create account
    query_db(
        " INSERT INTO user (email, password, first, last, phone, ssn) VALUES ('{}', '{}', '{}' , '{}' , '{}', '{}') ".format(
            email, password, first_name, last_name, phone_number, ssn
        ),
        is_update=True
    )

    return "New Account created!"


@app.route("/login", methods=['GET', 'POST'])
def login():

    def query_db(query, is_update=False):
        connection = mysql.connect()
        cursor = connection.cursor()
        res = []
        try:
            cursor.execute(query=query)
            if is_update:
                connection.commit()
            else:
                res = cursor.fetchall()
        except Exception as identifier:
            print(identifier)
        finally:
            cursor.close()
            connection.close()
        return res if not is_update else None

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
            print(identifier)
            print("Invalid data sent by the user")
            return "INVALID DATA SEND"

        if email and password:
            # Check if the user, password is valid in DB
            result = query_db(
                " select * from user where email= '{}' AND password = '{}' ".format(
                    email, password)
            )

            if len(result) == 0:
                return "INVALID USERNAME AND PASSWORD!"

            # Generate a random 5 digit CODE here
            CODE = ''.join(SAMPLE(DIGITS, 5))

            # Update DB of this email to store the code
            result = query_db(
                " UPDATE user as u SET u.code = '{}'  where u.email= '{}';".format(
                    CODE, email),
                is_update=True
            )

            # Send an email to the user with the code
            from smtplib import SMTP
            EMAIL_BODY = """Your code is {}.""".format(CODE)
            print(EMAIL_BODY)

            # Now send the EMail
            try:
                server = SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(DEV.GMAIL_USER, DEV.GMAIL_PASS)
                server.sendmail(DEV.GMAIL_USER, email, EMAIL_BODY)
                server.close()
                print("EMAIL SENT")
            except Exception as e:
                print(e)
                print('Something went wrong..., cannot send email')

            response = make_response(
                redirect(url_for("two_factor", email=email)), 302)

            return response

    return "Invalid Login Credentials"


def get_random_string(length):
    return ''.join(CHOICE(LOWERCASE) for i in range(length))


@app.route("/dashboard")
def dashboard():
    current_session = request.cookies.get("rrrr")
    if current_session:
        result = []
        # Check if there is a user or not for given session id
        try:
            conection = mysql.connect()
            cursor = conection.cursor()

            cursor.execute(
                " SELECT * from user where session= '{}' ".format(current_session))

            result = cursor.fetchall()

            cursor.close()
            conection.close()
        except Exception as identifier:
            print(identifier)
            print("Encountered an error connecting to MYSQL")
            return "MYSQL ERROR!"

        # Valid USER FOUND
        if len(result) > 0:
            return render_template("bankUser.html")

    return redirect(url_for("home"))


@app.route("/logout", methods=['GET'])
def log_user_out():

    def query_db(query, is_update=False):
        connection = mysql.connect()
        cursor = connection.cursor()
        res = []
        try:
            cursor.execute(query=query)
            if is_update:
                connection.commit()
            else:
                res = cursor.fetchall()
        except Exception as identifier:
            print(identifier)
        finally:
            cursor.close()
            connection.close()
        return res if not is_update else None

    # Get the user's info for logging out
    current_session = request.cookies.get("rrrr")
    if current_session:
        # Get the User's info
        result = query_db(
            "SELECT * FROM user WHERE session ='{}' ".format(current_session))

        if len(result) == 0:
            print("No USer is not logged in simply redirect")

        # Remove the session ID for the user in DB
        query_db(
            " UPDATE user SET session = NULL, code = NULL WHERE email='{}' ".format(
                result[0][0]),
            is_update=True
        )

        # Redirect to the login page
        response = make_response(redirect(url_for("home")), 302)

        # Expire the session cookie of the user
        response.set_cookie("rrrr", "", expires=0)

        return response
    else:
        # User is not logged in redirect to login page
        return redirect(url_for('home'))


@app.route("/twofactor", methods=['GET', 'POST'])
def two_factor():

    # Redirect to the second login page where the email is preset
    if request.method == "GET":
        email = request.args.get("email", None)
        if not email:
            return "Invalid URL"
        return render_template('two_factor.html', email=email)
    elif request.method == "POST":
        email = request.form.get("email", None)
        code = request.form.get("code", None)

        # Check if the code matches in the DB for the given email
        try:
            result = []
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(
                " SELECT * FROM user where email= '{}' AND code = '{}' ".format(
                    email, code)
            )
            result = cursor.fetchall()

        except Exception as identifier:
            print(identifier)
            print("Encountered an error connecting to MYSQL")
            return "MYSQL ERROR!"
        else:
            # Invalid code, notify the user
            if len(result) == 0:
                print("INVALID LOGIN ATTEMPT")
                return "INVALID LOGIN ATTEMPT"
        finally:
            cursor.close()
            conection.close()

        # Else return dashbord
        if email and code:
            print(email, code)
            response = make_response(
                redirect(url_for("dashboard")), 302)
            session_id = get_random_string(10)
            print("session", session_id)

            # Update the DB of the session ID
            try:
                conection = mysql.connect()
                cursor = conection.cursor()

                cursor.execute(
                    " UPDATE user SET session = '{}'  where email= '{}' AND code = '{}' ".format(session_id, email, code))

                cursor.close()
                conection.commit()
                conection.close()
            except Exception as identifier:
                print(identifier)
                print("Encountered an error connecting to MYSQL")
                return "MYSQL ERROR!"

            response.set_cookie("rrrr", session_id)
            return response

        return "HELLOO"


if __name__ == '__main__':
    app.run(debug=True)
