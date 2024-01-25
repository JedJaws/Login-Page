''' Midterm Project
Task 2: Error Handling
    ● Implement error handling for your API to ensure that it returns proper error
    messages and status codes.
    ● Create error handlers for ex. 400, 401, 404, 500, and any other errors that you feel
    are necessary.
    ● Make sure that error messages are returned in a consistent format.
Task 3: Authentication
    ● Implement authentication for your API using JWT Authentication.
    ● Create a user model with username and password fields.
    ● Implement a login endpoint that authenticates the user and returns a JWT token.
    ● Implement a protected endpoint that requires a valid JWT token to access.
Task 4: File Handling
    ● Implement file handling for your API to allow users to upload files.
    ● Create an endpoint that allows users to upload files.
    ● Implement file validation to ensure that only certain file types are allowed.
    ● Implement file size validation to ensure that files are uploaded within the allowed
    file size limit.
    ● Store uploaded files in a secure location. (A folder in your project's folder
    structure.)
Task 5: Public Route
    ● Create a public route that allows users to view public information.
    ● Implement an endpoint that returns a list of items that can be viewed publicly.
    ● Ensure that this endpoint does not require authentication
'''
from flask import Flask, render_template, request, redirect, url_for, session, abort
import pymysql
import re
from flask_cors import CORS

# (New) Importing flask_jwt_extended for JWT authentication
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# app.secret_key = 'secret'

# (New) setting up some configs for the flask_jwt_extended
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

# Establishing the connection to the MYSQL server
conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='1234567890',
        db='449_Midterm',
        cursorclass=pymysql.cursors.DictCursor
        )
cur = conn.cursor()

@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print('In Register')
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM accounts WHERE username= % s', (username))
        account = cur.fetchone()
        print(account)
        conn.commit()
        # Error Checking
        if account:
            msg = 'Account already exists'
        # Use regular expression to ensure only English letters and numbers are allowed
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username is not valid. Please use only english letters and numbers!'
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, % s, % s)', (username, password))
            conn.commit()
            print('Inserted into database')

            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    
    return render_template('register.html', msg = msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM accounts WHERE username = % s and password = % s', (username, password))
        conn.commit()
        account = cur.fetchone()
        msg = 'Successfully logged in'
        print('Success in login')
    else:
         msg = 'Incorrect username/password! '
         
    return render_template('login.html', msg = msg)

if __name__ == "__main__":
	app.run(host ="localhost", port = int("5000"), debug=True)