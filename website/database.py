import mysql.connector
db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'CINEPLEX',
    }

# Function to create a MySQL connection
def create_connection():
    return mysql.connector.connect(**db_config)

conn=create_connection()
# Create a cursor object to interact with the database
cursor = conn.cursor()

# Function to check if the database exists
def database_exists(cursor, database_name):
    query = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s"
    cursor.execute(query, (database_name,))
    return cursor.fetchone() is not None

def create_database_if_not_exists(cursor, database_name):
    if not database_exists(cursor, database_name):
        create_database_query = f"CREATE DATABASE {database_name}"
        cursor.execute(create_database_query)

# Create the database if it doesn't exist
database_name = 'CINEPLEX'
create_database_if_not_exists(cursor, database_name)

# Switch to the specified database
conn.database = database_name

# Close the cursor and connection
cursor.close()
conn.close()

############################################################################

# Check if the table exists before creating it
# Function to check if the table exists
def table_exists(table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

############################################################################
#creating users table in the db
conn=create_connection()
cursor=conn.cursor()

table_name = 'users'
if not table_exists(table_name):
    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE {table} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        phn_num VARCHAR(15) NOT NULL,
        email VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        amount INT 
    );
    """.format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

# Function to add a new user to the database
def add_user(name,phn_num,email,username,password):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (name, phn_num, email, username, password, amount) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (name, phn_num, email, username, password, 0))
    conn.commit()


    cursor.close()
    conn.close()

# Function to check if the user exists in the database
def check_user(email,password):
    conn = create_connection()
    cursor =conn.cursor()

    query='SELECT * FROM users WHERE email= %s AND password = %s'
    cursor.execute(query,(email,password))
    user=cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#User TABLE Done
############################################################################


############################################################################
# Creating Admin Table in the DB 
conn=create_connection()
cursor=conn.cursor()

table_name='admin'
if not table_exists(table_name):
    create_table_query = """
    CREATE TABLE {table} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Aname VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    );
    """.format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

# Function to add admin info to the db if it doesn't already exist
def add_admin_if_not_exists(name, email, username, password):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if admin with the same username already exists
    query_check = 'SELECT * FROM admin WHERE username = %s'
    cursor.execute(query_check, (username,))
    existing_admin = cursor.fetchone()

    if not existing_admin:
        # Admin doesn't exist, so insert the new admin
        query_insert = "INSERT INTO admin (Aname, email, username, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_insert, (name, email, username, password))
        conn.commit()

    cursor.close()
    conn.close()

#function to check if the admin exists in the DB 
def check_admin(username,password):
    conn=create_connection()
    cursor=conn.cursor()

    query='SELECT * FROM admin WHERE username= %s AND password = %s'
    cursor.execute(query,(username,password))
    admin_user=cursor.fetchone()

    cursor.close()
    conn.close()

    return admin_user

#Adding Admin Info to the DB
add_admin_if_not_exists('Habib','hrsiam421@gmail.com','hrsiam','Habib1234')
add_admin_if_not_exists('Nihal','nihal@gmail.com','INihal','Nihal1234')
add_admin_if_not_exists('Fahim','fahim@gmail.com','AFahim','Fahim1234')
add_admin_if_not_exists('Safi','safi@gmail.com','SSafi','Safi1234')

#Admin Table Done
############################################################################


############################################################################
#Creating Movie_info Table
conn=create_connection()
cursor=conn.cursor()

table_name='movie_info'
if not table_exists(table_name):
    create_table_query = """CREATE TABLE movie_info (
    movie_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255) NOT NULL UNIQUE KEY ,
    release_date DATE NOT NULL,
    director VARCHAR(255) NOT NULL,
    cast VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    language VARCHAR(255) NOT NULL,
    poster_image VARCHAR(255)
    );
    """.format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

#Function to add movie info data to the DB
def add_movie_info(movie_name, release_date, director, cast, genre, language, poster_image):
    conn=create_connection()
    cursor=conn.cursor()

    # Check if movie with the same director already exists
    query_check = 'SELECT * FROM movie_info WHERE movie_name = %s and director=%s'
    cursor.execute(query_check, (movie_name,director))
    existing_movie = cursor.fetchone()

    if not existing_movie:
        # Movie doesn't exist, so insert the new movie
        query="INSERT INTO movie_info (movie_name, release_date, director, cast, genre, language, poster_image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query,(movie_name, release_date, director, cast, genre, language, poster_image))
        conn.commit()

    cursor.close()
    conn.close()

add_movie_info("The Shawshank Redemption", "1994-09-14", "Frank Darabont", "Tim Robbins, Morgan Freeman, Bob Gunton", "Drama", "English", "https://images.app.goo.gl/owqtUzsHMpxDPrqS7")
add_movie_info("The Godfather", "1972-03-24", "Francis Ford Coppola", "Marlon Brando, Al Pacino, James Caan", "Crime, Drama", "English", "https://images.app.goo.gl/MKorXCamAT8VaUhq7")
add_movie_info("The Dark Knight", "2008-07-16", "Christopher Nolan", "Christian Bale, Michael Caine, Heath Ledger", "Action, Crime, Drama", "English", "https://images.app.goo.gl/f9zWtpsQWVj2tCcn9")
add_movie_info("Surongo", "2023-06-29", "Raihan Rafi", "Afran Nisho, Toma Mirza ,Shahiduzzaman Selim", "Adventure, Drama, Fantasy", "Bangla", "https://images.app.goo.gl/keTMUnnALuycXQtr5")
add_movie_info("Pulp Fiction", "1994-09-14", "Quentin Tarantino", "John Travolta, Samuel L. Jackson, Uma Thurman", "Crime, Drama", "English", "https://images.app.goo.gl/xQkaZuyMpXsevFrJ7")
add_movie_info('Oppenheimer', '2023-07-21', 'Christopher Nolan', 'Cillian Murphy, Emily Blunt, Matt Damon', 'Drama, History', 'English', 'https://images.app.goo.gl/Bu6evHReDTEQnrVd8')
add_movie_info('Jawan', '2023-06-02', 'Atlee', 'Shah Rukh Khan, Nayanthara, Vijay Sethupathi', 'Action, Thriller', 'Hindi, Tamil', 'https://images.app.goo.gl/kH5M1ugBnXWYNp3t5')


#Movie_info Table Done
############################################################################


############################################################################
#Creating Hall Table
conn=create_connection()
cursor=conn.cursor()

table_name='Hall'
if not table_exists(table_name):
    create_table_query = """CREATE TABLE {table} (
    branch_name VARCHAR(255) NOT NULL,
    hall_num INT NOT NULL,
    seat_capacity INT NOT NULL,
    type VARCHAR(255) NOT NULL,
    PRIMARY KEY (branch_name,hall_num)
    );""".format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

#Function to add hall info data to the DB
def hall_info(branch_name,hall_num, seat_capacity, type):
    conn=create_connection()
    cursor=conn.cursor()

    # Check if branch with the same hall_num already exists
    query_check = 'SELECT * FROM hall WHERE branch_name = %s and hall_num=%s'
    cursor.execute(query_check, (branch_name,hall_num))
    existing_movie = cursor.fetchone()

    if not existing_movie:
        query="INSERT INTO hall (branch_name,hall_num, seat_capacity, type) VALUES (%s, %s, %s, %s)"
        cursor.execute(query,(branch_name,hall_num, seat_capacity, type))
        conn.commit()

    cursor.close()
    conn.close()

hall_info('Mirpur',1,115,'VIP')
hall_info('Mirpur',2,350,'Regular')
hall_info('Mirpur',3,250,'Premium')
hall_info('Savar',1,250,'Premium')
hall_info('Savar',2,300,'Premium')
hall_info('Uttora',1,250,'Premium')
hall_info('Uttora',2,300,'Regula')
hall_info('Uttora',3,120,'VIP')
hall_info('Mohakhali',1,300,'Regular')
hall_info('Mohakhali',2,225,'Premium')
hall_info('Basundhara',1,250,'Premium')
hall_info('Basundhara',2,100,'VIP')

#Hall Table Done
############################################################################


############################################################################
#Creating Running_show table
conn=create_connection()
cursor=conn.cursor()

table_name='running_show'
if not table_exists(table_name):
    create_table_query = """CREATE TABLE running_show (
    show_ID INT PRIMARY KEY AUTO_INCREMENT,
    branch_name VARCHAR(255) NOT NULL,
    hall_num INT NOT NULL,
    movie_name VARCHAR(255) NOT NULL,
    show_time DATETIME NOT NULL,
    FOREIGN KEY (branch_name,hall_num) REFERENCES hall(branch_name,hall_num),
    FOREIGN KEY (movie_name) REFERENCES movie_info(movie_name)
    );
    """.format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

# Function to add movie and time data to the DB
def add_running_show(branch_name, hall_num, movie_name, show_time):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the running show already exists
    cursor.execute("""
            SELECT show_ID
            FROM running_show
            WHERE branch_name = %s AND hall_num = %s AND movie_name = %s AND show_time = %s
        """, (branch_name, hall_num, movie_name, show_time))

    existing_show = cursor.fetchone()

    if existing_show:
            pass
    else:
        # Check if the movie exists in the movie_info table
        cursor.execute("SELECT movie_name FROM movie_info WHERE movie_name = %s", (movie_name,))
        existing_movie = cursor.fetchone()

        if existing_movie:
            # Check if the hall exists in the hall table
            cursor.execute("SELECT hall_num FROM hall WHERE branch_name = %s AND hall_num = %s", (branch_name, hall_num))
            existing_hall = cursor.fetchone()

            if existing_hall:
                # Insert the running show
                query = "INSERT INTO running_show (branch_name, hall_num, movie_name, show_time) VALUES (%s, %s, %s, %s)"
                values = (branch_name, hall_num, movie_name, show_time)
                cursor.execute(query, values)
                conn.commit()

    cursor.close()
    conn.close()


#Function to delete any movie from the table
def rem_running_show(branch_name, hall_num, movie_name, show_time):
    conn = create_connection()
    cursor = conn.cursor()

    query = "DELETE FROM running_show WHERE branch_name = %s AND hall_num = %s AND movie_name = %s AND show_time = %s"
    values = (branch_name, hall_num, movie_name, show_time)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

add_running_show("Basundhara", 1, "The Shawshank Redemption", "2023-12-08 19:00:00")
add_running_show("Basundhara", 2, "The Godfather", "2023-11-28 17:00:00")
add_running_show("Mirpur", 1, "Surongo", "2023-11-29 17:00:00")
add_running_show("Mirpur", 2, "Pulp Fiction", "2023-11-29 14:30:00")
add_running_show("Mirpur", 3, "Oppenheimer", "2023-11-30 19:00:00")
add_running_show("Mohakhali", 1, "Jawan", "2023-12-01 17:00:00")
add_running_show("Mohakhali", 2, "The Dark Knight", "2023-12-10 17:00:00")
add_running_show("Savar", 1, "Pulp Fiction", "2023-12-15 15:00:00")
add_running_show("Savar", 2, "Jawan", "2023-12-08 17:00:00")
add_running_show("Uttora", 1, "Surongo", "2023-12-08 19:00:00")
add_running_show("Uttora", 2, "Godfather", "2023-12-08 15:00:00")
add_running_show("Uttora", 3, "The Dark Knight", "2023-12-14 14:30:00")
rem_running_show("Uttora", 3, "The Dark Knight", "2023-12-14 14:00:00")


#Running_show Table Done
############################################################################


############################################################################
#Creating booked_seats table
conn=create_connection()
cursor=conn.cursor()

table_name='booked_seats'
if not table_exists(table_name):
    create_table_query = """CREATE TABLE booked_seats (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    showtime_id INT NOT NULL,
    seat_row INT NOT NULL,
    seat_number INT NOT NULL,
    booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (showtime_id) REFERENCES running_show(show_ID)
    );
    """.format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

#Function to check whether a seat available or not
def is_seat_available(showtime_id, seat_row, seat_number):
    conn = create_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM booked_seats WHERE showtime_id = %s AND seat_row = %s AND seat_number = %s
    """
    values = (showtime_id, seat_row, seat_number)

    cursor.execute(query, values)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    # If there is a result, the seat is already booked; otherwise, it's available
    return result is None


#Function to booked a seat
def book_seat(user_id, showtime_id, seat_row, seat_number):
    conn = create_connection()
    cursor = conn.cursor()

    result=is_seat_available(showtime_id, seat_row, seat_number)
    if result:
        query = """
        INSERT INTO booked_seats (user_id, showtime_id, seat_row, seat_number)
        VALUES (%s, %s, %s, %s)
        """
        values = (user_id, showtime_id, seat_row, seat_number)

        cursor.execute(query, values)
        conn.commit()
    else:
        print("NOT")
    cursor.close()
    conn.close()
# book_seat(1,1,1,12)
#Booked_seats Table Done
############################################################################


############################################################################
#Creating Deposite table
conn=create_connection()
cursor=conn.cursor()

table_name='deposite'
if not table_exists(table_name):
    create_table_query = """CREATE TABLE deposite (
        Depo_ID INT AUTO_INCREMENT PRIMARY KEY,
        UID INT NOT NULL,
        Amount INT NOT NULL,
        Time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (UID) REFERENCES users(id)
    );""".format(table=table_name)

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

#Function to add deposite
def add_deposite(userId,amount):
    conn=create_connection()
    cursor=conn.cursor()

    query="INSERT INTO deposite (UID,amount) VALUES (%s, %s)"
    cursor.execute(query,(userId,amount))
    conn.commit()

    cursor.close()
    conn.close()
    
# add_deposite(1,1000)
#depostie Table Done
############################################################################


############################################################################
#Creating transaction table
conn = create_connection()
cursor = conn.cursor()

table_name = 'transaction'
if not table_exists(table_name):
    create_table_query = """CREATE TABLE `transaction` (
        trns_Id INT AUTO_INCREMENT PRIMARY KEY,
        Depo_id INT ,
        Book_id INT ,
        userId INT NOT NULL,
        type VARCHAR(20) NOT NULL,
        `Time` DATETIME DEFAULT CURRENT_TIMESTAMP,
        ticket_num VARCHAR(20) ,
        FOREIGN KEY (userId) REFERENCES users(id),
        FOREIGN KEY (Depo_id) REFERENCES deposite(Depo_ID),
        FOREIGN KEY (Book_id) REFERENCES booked_seats(booking_id)
    );"""

    cursor.execute(create_table_query)
    conn.commit()

cursor.close()
conn.close()

#Function to add transaction
def add_transactiondBYBooking(Book_id,userId,ticket_num):
    conn=create_connection()
    cursor=conn.cursor()

    query="INSERT INTO transaction (Book_id,userId,type,ticket_num) VALUES (%s, %s, %s,%s)"
    cursor.execute(query,(Book_id,userId,'Purchase Ticket',ticket_num))
    conn.commit()

    cursor.close()
    conn.close()

def add_transactiondBYDeposite(Depo_id,userId):
    conn=create_connection()
    cursor=conn.cursor()

    query="INSERT INTO transaction (Depo_id,userId,type) VALUES (%s, %s, %s)"
    cursor.execute(query,(Depo_id,userId,'Deposite Amount'))
    conn.commit()

    cursor.close()
    conn.close()

# add_transactiondBYBooking(3,1,'1/1')
# add_transactiondBYDeposite(3,1)

#transaction Table Done
############################################################################
