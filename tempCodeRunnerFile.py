from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# First set the variable in your environment before running:
# set MAILJET_API_KEY=your_public_key
# set MAILJET_SECRET_KEY=your_secret_key
MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.getenv('MAILJET_API_SECRET')
print("📧 API Key:", MAILJET_API_KEY)
print("📧 API Secret:", MAILJET_SECRET_KEY)


# Configure with your Mailjet API key
FROM_EMAIL = 'anshul.saini1507@gmail.com'  # Make sure this email is verified with Mailjet
FROM_NAME = 'Prescription System'

def send_mailjet_email(email, medicine):
    """Send medication reminder email using Mailjet API."""
    time_now = datetime.now().strftime("%H:%M:%S")
    subject = f"💊 Reminder: {medicine['name']} at {time_now}"

    html_body = f"""
    <h3>This is your reminder email from the Prescription System</h3>
    <p><b>Medicine:</b> {medicine['name']}</p>
    <p><b>Dosage:</b> {medicine['dosage']}</p>
    <p><b>Time:</b> {medicine['time']}</p>
    <br>
    <small>This is an automated reminder for your medication.</small>
    """

    url = "https://api.mailjet.com/v3.1/send"
    headers = {"Content-Type": "application/json"}
    payload = {
        "Messages": [
            {
                "From": {
                    "Email": FROM_EMAIL,
                    "Name": FROM_NAME
                },
                "To": [
                    {
                        "Email": email,
                        "Name": "Patient"
                    }
                ],
                "Subject": subject,
                "HTMLPart": html_body
            }
        ]
    }

    print(f"📤 Sending reminder to {email}...")
    response = requests.post(url, auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), headers=headers, json=payload)

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON response:")
        print(response.text)
        return

    if response.status_code == 200:
        print("✅ Email sent successfully!")
        print("📨 Message ID(s):", [m.get('To')[0].get('MessageUUID') for m in response_data.get('Messages', [])])
    else:
        print(f"❌ Failed to send email. Status Code: {response.status_code}")
        print("🔧 Response:", response_data)

@app.route('/')
def index():
    return render_template('prescription.html')

@app.route('/test')
def test_api_page():
    """Serve the API testing page"""
    return render_template('test_api.html')

@app.route('/api/schedule', methods=['POST'])
def schedule_reminders():
    data = request.get_json()
    email = data['email']
    
    for medicine in data['medicines']:
        start_time = datetime.strptime(medicine['time'], '%H:%M')
        
        # Schedule for each day of treatment
        for day in range(medicine['days']):
            trigger_time = datetime.now().replace(
                hour=start_time.hour,
                minute=start_time.minute
            ) + timedelta(days=day)
            
            # Reschedule if time has passed today
            if trigger_time < datetime.now():
                trigger_time += timedelta(days=1)
            
            scheduler.add_job(
                send_mailjet_email,
                'date',
                run_date=trigger_time,
                args=[email, medicine]
            )
            print(f"⏰ Scheduled email for '{medicine['name']}' at {trigger_time}")
    print("🧠 All current jobs in scheduler:")
    for job in scheduler.get_jobs():
        print(job)
    
    return jsonify({'status': 'success', 'message': 'Reminders scheduled successfully!'})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
