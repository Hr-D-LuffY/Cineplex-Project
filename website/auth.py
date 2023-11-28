from flask import Blueprint, render_template , redirect, url_for,request , flash ,session
from .database import *

auth = Blueprint('auth',__name__)

@auth.route('/signup' , methods=['GET','POST'])
def signup():
    if request.method== 'POST':
        name=request.form.get('name')
        phn_num=request.form.get('mobnum')
        email= request.form.get("email")
        username=request.form.get('username')
        pass1=request.form.get('pass1')
        pass2=request.form.get('pass2')

        if len(name) < 2:
            flash('Your name is too short or you make a mistake!!!',category='error')
        elif len(username) < 3:
            flash('Username must be greater than 4 characters',category='error')
        elif pass1 != pass2:
            flash("Password didn't match!!! Try again", category='error')
        elif len(pass1) <7:
            flash("Password must be greater than 7!!!", category='error')
        else:
            # add to database
            conn=create_connection()
            cursor=conn.cursor()

            query='SELECT * FROM users WHERE email = %s'
            cursor.execute(query,(email,))
            existing_user= cursor.fetchone()

            

            if existing_user:
                error='Email already connected to another account. PLease choose a diff email!'
                flash('Email already connected to another account. PLease choose a diff email!',category='error')
                return render_template('signup.html',error=error)
            else:
                add_user(name,phn_num,email,username, pass1)
                flash('Account Created!',category='success')

            cursor.close()
            conn.close()

    return render_template("signup.html")

@auth.route('/login' , methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        user = check_user(email,password)

        if user:
            # Store user information in the session
            session['user_id'] = user[0]
            session['username'] = user[1]
            print('success')
            flash('u just login',category='success')
            # return redirect(url_for('auth.signup'))
        else:
            flash('Invalid email or password',category='error')
            return render_template('login.html')
    
    return render_template("login.html")

@auth.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        user = check_admin(username,password)

        if user:
            # Store user information in the session
            session['user_id'] = user[0]
            session['username'] = user[1]
            print('success')
            flash('u just login',category='success')
            return redirect(url_for('views.adminpanel',id=session['user_id']))
        else:
            flash('Invalid username or password',category='error')
            return render_template('login.html')

    return render_template("admin.html")