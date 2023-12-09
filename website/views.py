from flask import Blueprint, render_template,request,flash,redirect,url_for
from .database import *
from datetime import datetime

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return redirect(url_for('auth.login'))
    # return render_template("login.html")

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

@views.route('/deposite_box/<id>', methods=["GET","POST"])
def deposite_box(id):
    conn=create_connection()
    cursor=conn.cursor()
    query='SELECT * FROM deposite'
    cursor.execute(query)
    deposite=cursor.fetchall()
    return render_template('deposite_box.html',user=deposite,id=id)

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

@views.route('/dashboard/<id>', methods=["GET", "POST"])
def dashboard(id):
    user = check_userByID(id)
    location = running_showBranch()

    if request.method == "POST":
        selected = request.form.get("location")
        loccon=True
        movies = running_movie_in_hall(selected)
        return render_template("dashboard.html",loccon=loccon, movies=movies, user=user, locations=location, id=id, selectedl=selected)
    
    return render_template("dashboard.html", user=user, locations=location, id=id)

@views.route('/dashboard/<id>/<location>', methods=["GET", "POST"])
def dashboard2(id,location):
    user = check_userByID(id)
    movies = running_movie_in_hall(location)
    if request.method=="POST":
        selectedmovie=request.form.get('selectedmovie')
        moviecon=True
        movieinfo=show_movie_info(selectedmovie)
        hallshowinfo=hall_time(location,selectedmovie)
        return render_template("dashboard2.html",moviecon=moviecon,movieinfo=movieinfo,selectmovie=selectedmovie,hallshowinfo=hallshowinfo, user=user,movies=movies, location=location, id=id)
    return render_template("dashboard2.html", user=user,movies=movies, location=location, id=id)

@views.route('/dashboard/<id>/<location>/<movie>', methods=["GET", "POST"])
def dashboard3(id,location,movie):
    user = check_userByID(id)
    hallshowinfo=hall_time(location,movie)
    movieinfo=show_movie_info(movie)

    if request.method=="POST":
        selectedshow=request.form.get('selectedshow')
        selectedcolumn=request.form.get("selectedcolumn")
        selectedrow=request.form.get("selectedrow")
        seat=f"{selectedrow}-{selectedcolumn}"
        showid=int(selectedshow[-3:-1])
        hallno=int(selectedshow[1])
        halltype=chck_hall_type(location,hallno)
        halltype=halltype[0]
        if halltype=="VIP":
            amount=800
        elif halltype=="Premium":
            amount=500
        else:
            amount=350
        datetime=getshowtime(showid)
        for dt_tuple in datetime:
            dt = dt_tuple
            showdate = dt.strftime('%Y-%m-%d')
            showtime = dt.strftime('%I:%M %p')
        seatresult=is_seat_available(showid,selectedrow,selectedcolumn)
        if seatresult:
            condition=True
        else:
            condition=False

        return render_template("dashboard3.html",showid=showid,showtime=showtime,showdate=showdate,seat=seat,amount=amount,halltype=halltype,condition=condition,hallno=hallno,movieinfo=movieinfo,selectmovie=movie, user=user, location=location,movie=movie, id=id,hallshowinfo=hallshowinfo)
    return render_template("dashboard3.html",movieinfo=movieinfo,selectmovie=movie, user=user, location=location, id=id,hallshowinfo=hallshowinfo,movie=movie)

@views.route('/purchase/<id>/<location>/<movie>/<showid>/<hallno>/<showdate>/<showtime>/<seat>', methods=["GET", "POST"])
def purchase(id,location,movie,showid,hallno,showdate,showtime,seat):
    user = check_userByID(id)
    print(user[-1])
    hallshowinfo=hall_time(location,movie)
    movieinfo=show_movie_info(movie)
    halltype=chck_hall_type(location,hallno)
    halltype=halltype[0]
    if halltype=="VIP":
            amount=800
    elif halltype=="Premium":
            amount=500
    else:
            amount=350

    if request.method=="POST":
        conditon=True
        seatrow=seat[0]
        seatcol=int(seat[2:])
        ticket_num=f"{seatrow}-{seatcol}"
        if user[-1]>amount:   
            book_seat(id,showid,seatrow,seatcol)
            booking_id=getbookId(id,showid,seatrow,seatcol)
            booking_id=int(booking_id[0])
            add_transactiondBYBooking(booking_id,id,ticket_num)
            cutmoney(id,amount)
            return render_template("purchase.html",moneycon=True,conditon=conditon,hallno=hallno ,halltype=halltype,seat=seat,showtime=showtime,showdate=showdate,amount=amount,movieinfo=movieinfo, user=user, location=location, id=id,hallshowinfo=hallshowinfo)
        else:
            return render_template("purchase.html",moneycon=False,conditon=conditon,hallno=hallno ,halltype=halltype,seat=seat,showtime=showtime,showdate=showdate,amount=amount,movieinfo=movieinfo, user=user, location=location, id=id,hallshowinfo=hallshowinfo)
    return render_template("purchase.html",hallno=hallno ,halltype=halltype,seat=seat,showtime=showtime,showdate=showdate,amount=amount,movieinfo=movieinfo, user=user, location=location, id=id,hallshowinfo=hallshowinfo)

@views.route('/profile/<id>',methods=["GET","POST"])
def profile(id):
    user=check_userByID(id)
    return render_template("profile.html",user=user, id=id)

@views.route('/mytransaction/<id>',methods=["GET","POST"])
def profileTransaction(id):
    user=check_userByID(id)
    transaction=gettransaction(id)
    return render_template("profile_transaction.html",transaction=transaction,user=user, id=id)

@views.route('/editprofile/<id>',methods=["GET","POST"])
def editProfile(id):
    user=check_userByID(id)
    if request.method=="POST":
        username = request.form.get('username')
        mobnum = request.form.get('mobnum')

        updateProfile(id,username,mobnum)
        condition=True
        return render_template("editprofile.html",condition=condition,user=user, id=id)
    return render_template("editprofile.html",user=user, id=id)

@views.route('/update_password/<id>', methods=["GET","POST"])
def updatepassword(id):
    user=check_userByID(id)
    if request.method=="POST":
        opassword= request.form.get('opassword')
        npassword= request.form.get('npassword')
        conpasword= request.form.get('conpassword')
        user=check_userByID(id)
        print(user[5])
        if user[5]==opassword and npassword==conpasword:
            updatePassword(npassword,id)
            flash("Your Password has been Changed",category='success')
            return render_template('update-password.html',user=user, id=id)
        elif user[5]!=opassword:
            flash("Old Password doesn't match",category='error')
            return render_template('update-password.html',user=user, id=id)
        elif npassword!=conpasword:
            flash("New Password doesn't match",category='error')
            return render_template('update-password.html',user=user, id=id)
    return render_template('update-password.html',user=user, id=id)

@views.route('/deposite/<id>',methods=["GET","POST"])
def deposite(id):
    user=check_userByID(id)
    if request.method=="POST":
        deposite_money= request.form.get('deposite_money')
        user=check_userByID(id)
        
        print(user[5])
        if int(deposite_money)>0:
            depositemoney(id,deposite_money)
            add_deposite(id,deposite_money)
            Depo_id=getdepoID(id)
            Depo_id=int(Depo_id[0])
            add_transactiondBYDeposite(Depo_id,id)
            user=check_userByID(id)
            return redirect(url_for('views.profile',user=user,id=id))
    return render_template("deposite.html",user=user,id=id)

