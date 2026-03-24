import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Security: Ensure MONGO_URI is set in Vercel Settings
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.vibe_db
collection = db.updates

@app.route('/')
def index():
    # Fetch posts from MongoDB, newest first
    posts = list(collection.find().sort("_id", -1))
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    skill = request.form.get('skill')
    notes = request.form.get('notes')
    if skill:
        collection.insert_one({
            "skill": skill,
            "notes": notes,
            "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
        })
    return redirect('/')

# Required for Vercel deployment
if __name__ == '__main__':
    app.run(debug=True)