from flask import Flask, render_template,request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="261205",  
    database="tailoring_app"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/About')
def about():
    return render_template("About.html")
@app.route('/Services')
def Services():
    return render_template("Services.html")
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        service = request.form.get('service')
        date = request.form.get('date')
        details = request.form.get('details')

        query = "INSERT INTO booking (name, phone, service, date, details) VALUES (%s, %s, %s, %s, %s)"
        values = (name, phone, service, date, details)

        cursor.execute(query, values)
        db.commit()

        order_id = cursor.lastrowid  

        return f"""
        <script>
        alert("Booking Submitted Successfully! Your Order ID: {order_id}");
        window.location.href = "/";
        </script>
        """

    return render_template("booking.html")
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        query = "INSERT INTO contact_messages (name, email, phone, message) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, message)

        cursor.execute(query, values)
        db.commit()

        return """
        <script>
        alert("Message Saved Successfully!");
        window.location.href = "/contact";
        </script>
        """

    return render_template("contact.html")
@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM booking")
    bookings = cursor.fetchall()


    cursor.execute("SELECT * FROM contact_messages")
    contacts = cursor.fetchall()

    return render_template("admin.html", bookings=bookings, contacts=contacts)



if __name__ == '__main__':
    app.run(debug=True)
