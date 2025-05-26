from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Alumni
from config import Config
from sqlalchemy import func
from datetime import datetime
import sys
import json
from sheets_integration import fetch_and_update_alumni

app = Flask(__name__)
app.config.from_object(Config)

try:
    db.init_app(app)
except Exception as e:
    print(f"Database initialization error: {str(e)}", file=sys.stderr)
    sys.exit(1)

# Route to display the Google Form
@app.route('/alumni/register', methods=['GET', 'POST'])
def alumni_register():
    if request.method == 'POST':
        try:
            # Convert date string to date object
            date_of_birth = None
            if request.form.get('date_of_birth'):
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

            # Convert years of experience to integer
            years_of_experience = None
            if request.form.get('years_of_experience'):
                try:
                    years_of_experience = int(request.form['years_of_experience'])
                except ValueError:
                    years_of_experience = None

            alumni = Alumni(
                # Basic Information
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form.get('phone', ''),
                date_of_birth=date_of_birth,
                gender=request.form.get('gender', ''),

                # Education Details
                degree=request.form['degree'],
                department=request.form['department'],
                graduation_year=int(request.form['graduation_year']),
                student_id=request.form['student_id'],

                # Professional Information
                current_employer=request.form.get('current_employer', ''),
                job_title=request.form.get('job_title', ''),
                industry=request.form.get('industry', ''),
                years_of_experience=years_of_experience,
                linkedin=request.form.get('linkedin', ''),

                # Location
                current_city=request.form.get('current_city', ''),
                state=request.form.get('state', ''),
                country=request.form.get('country', ''),

                # Skills and Interests
                technical_skills=request.form.get('technical_skills', ''),
                languages_known=request.form.get('languages_known', ''),
                areas_of_interest=request.form.get('areas_of_interest', '')
            )
            
            db.session.add(alumni)
            db.session.commit()
            flash('Registration successful! Welcome to the alumni network.', 'success')
            return redirect(url_for('alumni_profile', id=alumni.id))
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
    
    return render_template('alumni_register.html')

# API endpoint to receive Google Form submissions
@app.route('/api/alumni/submit', methods=['POST'])
def receive_alumni_submission():
    try:
        data = request.get_json()
        
        # Convert date string to date object
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                date_of_birth = datetime.strptime(data['date_of_birth'], '%m/%d/%Y').date()
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

@app.route('/')
def dashboard():
    total_alumni = Alumni.query.count()
    recent_alumni = Alumni.query.order_by(Alumni.created_at.desc()).limit(5).all()
    graduation_years = db.session.query(
        Alumni.graduation_year, 
        func.count(Alumni.id)
    ).group_by(Alumni.graduation_year).all()
    
    return render_template('dashboard.html',
                         total_alumni=total_alumni,
                         recent_alumni=recent_alumni,
                         graduation_years=graduation_years)

@app.route('/alumni')
def alumni_list():
    alumni = Alumni.query.order_by(Alumni.last_name).all()
    return render_template('alumni_list.html', alumni=alumni)

@app.route('/alumni/<int:id>')
def alumni_profile(id):
    alumni = Alumni.query.get_or_404(id)
    return render_template('alumni_profile.html', alumni=alumni)

@app.route('/alumni/add', methods=['GET', 'POST'])
def add_alumni():
    if request.method == 'POST':
        try:
            # Convert date string to date object
            date_of_birth = None
            if request.form.get('date_of_birth'):
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

            # Convert years of experience to integer
            years_of_experience = None
            if request.form.get('years_of_experience'):
                try:
                    years_of_experience = int(request.form['years_of_experience'])
                except ValueError:
                    years_of_experience = None

            alumni = Alumni(
                # Basic Information
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form.get('phone', ''),
                date_of_birth=date_of_birth,
                gender=request.form.get('gender', ''),

                # Education Details
                degree=request.form['degree'],
                department=request.form['department'],
                graduation_year=int(request.form['graduation_year']),
                student_id=request.form['student_id'],

                # Professional Information
                current_employer=request.form.get('current_employer', ''),
                job_title=request.form.get('job_title', ''),
                industry=request.form.get('industry', ''),
                years_of_experience=years_of_experience,
                linkedin=request.form.get('linkedin', ''),

                # Location
                current_city=request.form.get('current_city', ''),
                state=request.form.get('state', ''),
                country=request.form.get('country', ''),

                # Skills and Interests
                technical_skills=request.form.get('technical_skills', ''),
                languages_known=request.form.get('languages_known', ''),
                areas_of_interest=request.form.get('areas_of_interest', '')
            )
            db.session.add(alumni)
            db.session.commit()
            flash('Alumni added successfully!', 'success')
            return redirect(url_for('alumni_list'))
        except Exception as e:
            flash(f'Error adding alumni: {str(e)}', 'error')
    
    return render_template('alumni_form.html', current_year=datetime.now().year)

@app.route('/alumni/<int:id>/edit', methods=['GET', 'POST'])
def edit_alumni(id):
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # Convert date string to date object
            date_of_birth = None
            if request.form.get('date_of_birth'):
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

            # Convert years of experience to integer
            years_of_experience = None
            if request.form.get('years_of_experience'):
                try:
                    years_of_experience = int(request.form['years_of_experience'])
                except ValueError:
                    years_of_experience = None

            # Basic Information
            alumni.first_name = request.form['first_name']
            alumni.last_name = request.form['last_name']
            alumni.email = request.form['email']
            alumni.phone = request.form.get('phone', '')
            alumni.date_of_birth = date_of_birth
            alumni.gender = request.form.get('gender', '')

            # Education Details
            alumni.degree = request.form['degree']
            alumni.department = request.form['department']
            alumni.graduation_year = int(request.form['graduation_year'])
            alumni.student_id = request.form['student_id']

            # Professional Information
            alumni.current_employer = request.form.get('current_employer', '')
            alumni.job_title = request.form.get('job_title', '')
            alumni.industry = request.form.get('industry', '')
            alumni.years_of_experience = years_of_experience
            alumni.linkedin = request.form.get('linkedin', '')

            # Location
            alumni.current_city = request.form.get('current_city', '')
            alumni.state = request.form.get('state', '')
            alumni.country = request.form.get('country', '')

            # Skills and Interests
            alumni.technical_skills = request.form.get('technical_skills', '')
            alumni.languages_known = request.form.get('languages_known', '')
            alumni.areas_of_interest = request.form.get('areas_of_interest', '')
            
            db.session.commit()
            flash('Alumni updated successfully!', 'success')
            return redirect(url_for('alumni_profile', id=alumni.id))
        except Exception as e:
            flash(f'Error updating alumni: {str(e)}', 'error')
    
    return render_template('alumni_form.html', alumni=alumni, current_year=datetime.now().year)

@app.route('/sync-sheets')
def sync_sheets():
    try:
        success = fetch_and_update_alumni()
        if success:
            flash('Successfully synced data from Google Sheets!', 'success')
        else:
            flash('Error syncing data from Google Sheets.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/alumni/<int:id>/delete', methods=['POST'])
def delete_alumni(id):
    try:
        alumni = Alumni.query.get_or_404(id)
        db.session.delete(alumni)
        db.session.commit()
        flash('Alumni deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting alumni: {str(e)}', 'error')
    return redirect(url_for('alumni_list'))

@app.route('/register')
def alumni_registration():
    return render_template('alumni_registration.html')

@app.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True)
    except Exception as e:
        print(f"Application startup error: {str(e)}", file=sys.stderr)
        sys.exit(1) 