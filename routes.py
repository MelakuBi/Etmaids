from app import app
from flask import render_template, flash, request, redirect, url_for, session, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField  
import urllib.request
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import os


app.secret_key = 'loginto'
mysql = MySQL(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_photo(photo):
    #photo = photoname + '.png'    
     extension = photo.filename.split(".")[-1]
     photoname = session['username'] + '.' + extension
     photoname = secure_filename(photoname)
     photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photoname))
    #file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
     return photoname

# Define your routes and views here
@app.route('/etmaids/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
        # Fetch one record and return result
    msg = cursor.fetchall()
    #msg = ('hello hello')
        # User is loggedin show them the home page
    return render_template('index.html', msg=msg)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/maids')
def Maids():
    return render_template('Maids.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/etmaids/Login', methods=['GET', 'POST'])
def Login():
     # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'phone' in request.form and 'password' in request.form:
        # Create variables for easy access
        phone = request.form['phone']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE phone = %s AND password = %s', (phone, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['First_Name'] = account['First_Name']
            # Redirect to home page
            msg = 'hey' + account['First_Name'] + 'You are Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Login.html', msg=msg)

#logout 
@app.route('/logout')
def logout():
    session.clear()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    msg = cursor.fetchall()
    
    return render_template('logout.html', msg=msg)


@app.route('/etmaids/Register', methods=['GET', 'POST'])
def registration():
    phone_regex = r'^0[79]\d{8}$'
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'username' in request.form and 'password' in request.form and 'phone' in request.form:
        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE phone = %s", [phone])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account and phone == account['phone']:
                msg = 'This phone number is already used please use another phone number!'
        elif not fname or not lname or not username or not password or not phone:
            msg = 'Please fill out the form correctly!'
        elif not re.match(phone_regex, phone):
            msg = 'invalid phone number!'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()

           # filename = secure_filename(photo.filename)
            #photo.save(os.path.join(app.config['UPLOAD_FOLDER'], username + '.jpg'))
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts (First_Name, Last_Name, username, password, phone) VALUES (%s, %s, %s, %s, %s)', (fname, lname, username, password, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return redirect(url_for('index', msg=msg))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('registration.html', msg=msg)

@app.route('/etmaids/profile_register', methods=['GET', 'POST'])
def profile_register():
    #file_path = ''
    if 'loggedin' in session:
        id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE id = %s", [id])
        msg = cursor.fetchone()
    if request.method == 'POST' and 'age' in request.form or 'religion' in request.form or 'city' in request.form or 'wcondition' in request.form or 'experience' in request.form or 'salary' in request.form or 'photo' in request.form:
        age = request.form['age']
        religion = request.form['religion']
        city = request.form['city']
        wcondition = request.form['wcondition']
        salary = request.form['salary']
        experience = request.form['experience']
        photo = request.files['photo']
        if photo and allowed_file(photo.filename) and 'loggedin' in session: 
            picture = photo          
            save_photo(photo)
            extension = picture.filename.split(".")[-1]
            photoname = session['username'] + '.' + extension
           # photoname = secure_filename(photoname)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "UPDATE accounts SET age=%s, religion=%s, residence=%s, wcondition=%s, salary=%s, experience=%s, photo=%s WHERE id=%s"
        val = (age, religion, city, wcondition, salary, experience, photoname, session['id'])
        cursor.execute(query, val)
        mysql.connection.commit()
           # cursor.close()
        msg = 'profile updated successfully'
        return redirect(url_for('home', msg=msg))
    else:
     return  render_template('profile_form.html', msg=msg)

# Display maids profile to view their information by themselves
@app.route('/etmaids/profile')
def profile_view():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
       # photo = ''
        #photo = account['First_Name'] + '.png'
        #file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo)
        #display = "return send_from_directory('uploads', photo, as_attachment=True)"
        #account['photo'] = file_path
        # Show the profile page with account info
        return render_template('profile.html', account=account)

           
    
@app.route('/etmaids/<id>')
def detail_view(id):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM accounts WHERE id = %s", [id])
            account = cursor.fetchone()
        
            return render_template('profile_detail_First.html', account=account)
           
    
# Take maids to their Home page on login    
@app.route('/etmaids/home')
def home():
    if 'loggedin' in session:
      usr = session['First_Name']
    return render_template('home.html', usr=usr)



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)