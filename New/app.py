from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


DATABASE = "data.db"

def create_table_if_not_exists():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            property_id TEXT,
            booking_date DATE,
            check_in_date DATE,
            checkout_date DATE,
            no_guests INTEGER,
            room_category TEXT,
            booking_platform TEXT,
            ratings_given INTEGER,
            booking_status TEXT,
            revenue_generated REAL
        )
    ''')
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

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (property_id, booking_date, check_in_date, checkout_date, no_guests, room_category, booking_platform, ratings_given, booking_status, revenue_generated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (property_id, booking_date, check_in_date, checkout_date, no_guests, room_category, booking_platform, ratings_given, booking_status, revenue_generated))
    conn.commit()
    conn.close()

    return redirect(url_for('data_entry_form'))

if __name__ == '__main__':
    app.run(debug=True)
