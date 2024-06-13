from flask import Flask, render_template, request, flash, session, redirect, url_for
import sqlite3
#functions 2  generate and check password password hashes
from werkzeug.security import generate_password_hash, check_password_hash

#ez create app
app = Flask(__name__)
#secret key needed gor sessions n' flash messages
app.secret_key = 'petersucksballs'

#the path and filename for the database
DATABASE = "skincare.db"

#function to auto connect and query
#took this code from older website i made
def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


#routes go here - this the bagosh homington
@app.route('/')
def index():
    return render_template('index.html')


#abort 404..... set a logout when user exits tab ect m8
@app.route('/login', methods=["GET","POST"])
def login():
    #if user posts a username and password
    if request.method == "POST":
        #get the username and password
        username = request.form['username']
        password = request.form['password']
        #try to find this user in the database
        sql = "SELECT * FROM user WHERE username = ?"
        user = query_db(sql=sql,args=(username,),one=True)
        if user:
            #wgot use
            #check password matches.............
            if check_password_hash(user[2],password):
                #we are logged in successfully
                #Store the username in the session
                session['user'] = user
                flash("Logged in successfully")
                return redirect('login')
            else:
                flash("invalid login attempt")
        else:
            flash("invalid login attempt")
    #render this template regardles of get/post
    return render_template('login.html')


@app.route('/signup', methods=["GET","POST"])
def signup():
    #if the user posts from the signup page
    if request.method == "POST":
        #add the new username and hashed password to the database
        username = request.form['username']
        password = request.form['password']
        #hash it with the secutiry function
        hashed_password = generate_password_hash(password)
        #write it as a new user to the database
        sql = "INSERT INTO user (username,password) VALUES (?,?)"
        query_db(sql,(username,hashed_password))
        #message flashes exist in the base.html template and give user feedback
        flash("Sign Up Successful")
        return redirect('signup')
    return render_template('signup.html')


@app.route('/products', methods=["GET","POST"])
def products():
    if 'user' in session:
        if request.method == 'POST':
            db = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            product_name = request.form['name']
            use_skincare = request.form['name']
            sql = "INSERT INTO product (name, use_skincare) VALUES (?,?)"
            query_db(sql,(product_name, use_skincare))
            results = cursor.fetchall()
            flash("did it work")
            return render_template('product.html', results=results)
        else:
            return render_template('product.html')
    flash("sign in pls u loser")
    return render_template("login.html")


@app.route('/logout')
def logout():
    #just clear the username from the session and redirect back to the home page
    #make it so when tab out user is out too 
    session['user'] = None
    return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    error = 'Page not found. Please check that the address is spelt correctly.'
    return render_template('error.html', error=error)


#   internal server error page
@app.errorhandler(500)
def internal_server_error(error):
    error = 'Internal server error.'
    return render_template('error.html', error=error)


#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)