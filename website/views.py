from flask import Blueprint, render_template,request,flash
from .database import *

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/adminpanel/<id>')
def adminpanel(id):
    conn=create_connection()
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM admin WHERE id = %s""", (id,))
    user = cursor.fetchone()
    return render_template("adminpanel.html",user=user)

@views.route('/addMovieInfo/<id>', methods=['GET','POST'])
def AddmovieInfo(id):
    if request.method== 'POST':
        Movie_name=request.form.get('Movie_name')
        Release_Date=request.form.get('Release_Date')
        Director= request.form.get("Director")
        Cast=request.form.get('Cast')
        Genre=request.form.get('Genre')
        Language=request.form.get('Language')
        Image_link=request.form.get('Image_link')

        # add to database
        conn=create_connection()
        cursor=conn.cursor()

        add_movie_info(Movie_name,Release_Date,Director,Cast,Genre,Language,Image_link)
        flash('Added New Movie Info!',category='success')

        cursor.close()
        conn.close()
    return render_template("add_movie_info.html",user=id)

@views.route('/addHallInfo/<id>', methods=['GET','POST'])
def AddHallInfo(id):
    if request.method== 'POST':
        Branch_name=request.form.get('Branch_name')
        Hall_no=request.form.get('Hall_no')
        Seat_Capacity= request.form.get("Seat_Capacity")
        Type=request.form.get('Type')

        # add to database
        conn=create_connection()
        cursor=conn.cursor()

        hall_info(Branch_name,Hall_no,Seat_Capacity,Type)
        flash('New Hall Added',category='success')

        cursor.close()
        conn.close()
    return render_template("add_hall.html",user=id)

@views.route('/userlist/<id>', methods=["GET","POST"])
def userlist(id):
    conn=create_connection()
    cursor=conn.cursor()
    query='SELECT * FROM users'
    cursor.execute(query)
    userslist=cursor.fetchall()
    return render_template('userlist.html',user=userslist,id=id)

@views.route('/deposite/<id>', methods=["GET","POST"])
def deposite(id):
    conn=create_connection()
    cursor=conn.cursor()
    query='SELECT * FROM deposite'
    cursor.execute(query)
    deposite=cursor.fetchall()
    return render_template('deposite.html',user=deposite,id=id)

@views.route('/transaction/<id>', methods=["GET","POST"])
def transaction(id):
    conn=create_connection()
    cursor=conn.cursor()
    query='SELECT * FROM transaction'
    cursor.execute(query)
    transaction=cursor.fetchall()
    return render_template('transaction.html',user=transaction,id=id)

@views.route('/booked_seat/<id>', methods=["GET","POST"])
def booked_seat(id):
    conn=create_connection()
    cursor=conn.cursor()
    query='SELECT * FROM booked_seats'
    cursor.execute(query)
    booked_seat=cursor.fetchall()
    return render_template('booked_seat.html',user=booked_seat,id=id)

@views.route('/addrunningShow/<id>', methods=['GET','POST'])
def addrunningShow(id):
    if request.method== 'POST':
        Branch_name=request.form.get('Branch_name')
        Hall_no=request.form.get('Hall_no')
        movie_name= request.form.get("movie_name")
        date= request.form.get("date")
        time=request.form.get('time')
        timing= f"{date} {time}:00"

        # add to database
        conn=create_connection()
        cursor=conn.cursor()

        add_running_show(Branch_name,Hall_no,movie_name,timing)
        flash('Added New Running Show',category='success')

        cursor.close()
        conn.close()
    return render_template("add_runningShow.html",user=id)

@views.route('/runningShowList/<id>', methods=["GET","POST"])
def runningShowList(id):
    if request.method=="POST":
        order_by = request.form.get('order_by')
        remove_button = request.form.get('remove_button')
        
        runningshow= running_showOrderByBranch()

        if remove_button :
            rem_running_show(remove_button)
            runningshow= running_showOrderByBranch()
            return render_template('running_show_list.html',user=runningshow,id=id)
        if order_by=="Movies_Name":
            runningshow=running_showOrderByMovie()
            return render_template('running_show_list.html',user=runningshow,id=id)
        elif order_by=="Branch_Name":
            runningshow= running_showOrderByBranch()
            return render_template('running_show_list.html',user=runningshow,id=id)
        else:
            runningshow= running_showOrderByBranch()
            return render_template('running_show_list.html',user=runningshow,id=id)
        
        
    return render_template('running_show_list.html', id=id)