from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import geocoder
from twilio.rest import Client
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# In-memory storage for users (for demonstration purposes)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    emergency_contacts = request.form['emergency_contacts'].split(',')
    users[username] = {
        'emergency_contacts': emergency_contacts,
        'last_location': None,
        'last_checkin': None
    }
    session['username'] = username  # Store the username in the session
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    username = session.get('username')
    if username in users:
        return render_template('profile.html', username=username, emergency_contacts=users[username]['emergency_contacts'])
    return redirect(url_for('index'))

@app.route('/checkin', methods=['POST'])
def checkin():
    username = session.get('username')
    if username in users:
        users[username]['last_checkin'] = datetime.now()
        users[username]['last_location'] = get_location()
        return redirect(url_for('profile'))
    return redirect(url_for('index'))

def get_location():
    g = geocoder.ip('me')
    return g.latlng  # Returns latitude and longitude

@app.route('/share_location', methods=['POST'])
def share_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    username = session.get('username')
    users[username]['last_location'] = (latitude, longitude)  # Store the last known location
    return jsonify({"status": "Location shared successfully!"})

@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    username = data['username']
    location = data['location']
    users[username]['last_location'] = location  # Update last known location
    send_alert(username)  # Send alert to emergency contacts
    return '', 204

def send_alert(username):
    user = users[username]
    emergency_contacts = user['emergency_contacts']
    last_location = user['last_location']  # Get the last known location

    # Twilio setup
    account_sid = 'your_account_sid'  # Replace with your Twilio account SID
    auth_token = 'your_auth_token'      # Replace with your Twilio auth token
    client = Client(account_sid, auth_token)

    for contact in emergency_contacts:
        message = client.messages.create(
            body=f"Alert! {username} is in distress! Last known location: {last_location}",
            from_='your_twilio_number',  # Replace with your Twilio phone number
            to=contact
        )

if __name__ == '__main__':
    app.run(debug=True)