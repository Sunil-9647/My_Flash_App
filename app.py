from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# --- MongoDB Atlas Configuration ---
# Fetch the URI securely from the environment variable
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['my_database']
collection = db['user_data']

# ==========================================
# Task 1: JSON API Route
# ==========================================
@app.route('/api', methods=['GET'])
def get_api_data():
    try:
        # Read the list of data from the backend file
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# Task 2: Frontend Form with MongoDB Atlas
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        # Get data submitted from the frontend form
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Validation checks
        if not name or not email:
            error = "Both Name and Email are required."
            return render_template('index.html', error=error)
            
        try:
            # Insert the data into MongoDB Atlas
            collection.insert_one({"name": name, "email": email})
            
            # On success: redirect to success page
            return redirect(url_for('success'))
            
        except PyMongoError as e:
            # On error: capture the database error to display on the same page
            error = f"Database error occurred: {str(e)}"
        except Exception as e:
            # On error: capture unexpected errors
            error = f"An unexpected error occurred: {str(e)}"
            
    # Render the same page, displaying any errors without redirecting
    return render_template('index.html', error=error)


@app.route('/success')
def success():
    # Success page route
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)