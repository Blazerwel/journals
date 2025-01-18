from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection settings (replace with your actual settings)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="journals_db"
)

# Pagination settings
per_page = 9

@app.route('/')
def home():
    cursor = db.cursor(dictionary=True)

    # Get total count of journals
    cursor.execute("SELECT COUNT(*) FROM journals")  # Corrected table name
    total_journals = cursor.fetchone()['COUNT(*)']

    # Calculate total pages
    total_pages = (total_journals + per_page - 1) // per_page

    # Fetch journal data for current page
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page
    cursor.execute("SELECT ID, Title, journal_URL, PDF_URL, Published_date, Actual_PDF, Created, Modified FROM journals LIMIT %s OFFSET %s", (per_page, offset))  # Corrected table name
    journal_data = cursor.fetchall()

    # Convert Actual_PDF to a string if necessary
    for journal in journal_data:
        journal['Actual_PDF'] = str(journal['Actual_PDF'])

    return render_template('index.html', journals=journal_data, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
