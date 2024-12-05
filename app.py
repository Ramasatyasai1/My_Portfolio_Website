from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="portfolio"
    )

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert the data
    try:
        cursor.execute(
            "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        connection.commit()
        return redirect(url_for('home'))  # Redirect to home after submission
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return "An error occurred. Please try again later."
    finally:
        cursor.close()
        connection.close()

# Route for navigation links
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/projects')
def projects():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('projects.html', projects=projects)

@app.route('/contact-info')
def contact_info():
    return render_template('contact_info.html', email="ramasatyasaithota@gmail.com", phone="9989360266")

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

    

