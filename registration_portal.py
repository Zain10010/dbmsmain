from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Alumni
from config import Config
from datetime import datetime
import sys

app = Flask(__name__)
app.config.from_object(Config)

try:
    db.init_app(app)
except Exception as e:
    print(f"Database initialization error: {str(e)}", file=sys.stderr)
    sys.exit(1)

@app.route('/')
def alumni_registration():
    return render_template('alumni_registration.html')

@app.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')

@app.route('/api/alumni/submit', methods=['POST'])
def receive_alumni_submission():
    try:
        data = request.get_json()
        
        # Convert date string to date object
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                date_of_birth = None

        # Convert years of experience to integer
        years_of_experience = None
        if data.get('years_of_experience'):
            try:
                years_of_experience = int(data['years_of_experience'])
            except ValueError:
                years_of_experience = None

        # Convert graduation year to integer
        graduation_year = None
        if data.get('graduation_year'):
            try:
                graduation_year = int(data['graduation_year'])
            except ValueError:
                graduation_year = None

        alumni = Alumni(
            # Basic Information
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone', ''),
            date_of_birth=date_of_birth,
            gender=data.get('gender', ''),

            # Education Details
            degree=data['degree'],
            department=data['department'],
            graduation_year=graduation_year,
            student_id=data['student_id'],

            # Professional Information
            current_employer=data.get('current_employer', ''),
            job_title=data.get('job_title', ''),
            industry=data.get('industry', ''),
            years_of_experience=years_of_experience,
            linkedin=data.get('linkedin', ''),

            # Location
            current_city=data.get('current_city', ''),
            state=data.get('state', ''),
            country=data.get('country', ''),

            # Skills and Interests
            technical_skills=data.get('technical_skills', ''),
            languages_known=data.get('languages_known', ''),
            areas_of_interest=data.get('areas_of_interest', '')
        )
        
        db.session.add(alumni)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Alumni data received successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        # Run on all network interfaces with explicit host and port
        print("Starting registration portal...")
        print("Access the portal at: http://172.20.10.2:5001")
        print("Make sure Windows Firewall allows connections on port 5001")
        app.run(host='172.20.10.2', port=5001, debug=True, threaded=True)
    except Exception as e:
        print(f"Application startup error: {str(e)}", file=sys.stderr)
        sys.exit(1) 