
from flask import Flask, request, jsonify, render_template
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

# Database setup
DATABASE = 'telecalling.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telecalling_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT,
            order_id TEXT,
            mobile_number TEXT,
            customer_name TEXT,
            address TEXT,
            order_amount REAL,
            product_name TEXT,
            error_reason TEXT,
            calling_date TEXT,
            agent_name TEXT,
            agent_remark TEXT,
            attempt_number TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Process Excel file and save data to the database
    data = pd.read_excel(file_path)
    conn = sqlite3.connect(DATABASE)
    data.to_sql('telecalling_data', conn, if_exists='append', index=False)
    conn.close()
    
    return jsonify({'success': 'File uploaded and data saved successfully'}), 200

# Route to fetch data from the database
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telecalling_data")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
