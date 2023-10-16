from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Update these variables with your MySQL server details
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"

# Define the name of the database you want to create
MYSQL_DB_NAME = "aghil"

def create_table_if_not_exists():
    # Create a MySQL connection and select the database
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME
    )
    cursor = conn.cursor()

    # Define the table creation SQL statement
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            property_id VARCHAR(255),
            booking_date DATE,
            check_in_date DATE,
            checkout_date DATE,
            no_guests INT,
            room_category VARCHAR(255),
            booking_platform VARCHAR(255),
            ratings_given INT,
            booking_status VARCHAR(255),
            revenue_generated FLOAT
        )
    '''

    # Execute the table creation query
    cursor.execute(create_table_query)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

@app.route('/')
def data_entry_form():
    create_table_if_not_exists()
    return render_template('entry.html')

from datetime import datetime

@app.route('/', methods=['POST'])
def submit_data():
    create_table_if_not_exists()
    property_id = request.form['property_id']
    booking_date = datetime.strptime(request.form['booking_date'], '%Y-%m-%d').date()
    check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d').date()
    checkout_date = datetime.strptime(request.form['checkout_date'], '%Y-%m-%d').date()
    no_guests = int(request.form['no_guests'])
    room_category = request.form['room_category']
    booking_platform = request.form['booking_platform']
    ratings_given = int(request.form['ratings_given'])
    booking_status = request.form['booking_status']
    revenue_generated = float(request.form['revenue_generated'])

    # Create a MySQL connection
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME
    )
    cursor = conn.cursor()

    # Execute the INSERT query with MySQL placeholders
    insert_query = '''
        INSERT INTO bookings (property_id, booking_date, check_in_date, checkout_date, no_guests, room_category, booking_platform, ratings_given, booking_status, revenue_generated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (property_id, booking_date, check_in_date, checkout_date, no_guests, room_category, booking_platform, ratings_given, booking_status, revenue_generated)

    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

    return redirect(url_for('data_entry_form'))

if __name__ == '__main__':
    app.run(debug=True)
