from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Basic Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))

    # Education Details
    degree = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)

    # Professional Information
    current_employer = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    years_of_experience = db.Column(db.Integer)
    linkedin = db.Column(db.Text)

    # Location
    current_city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))

    # Skills and Interests
    technical_skills = db.Column(db.Text)
    languages_known = db.Column(db.Text)
    areas_of_interest = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Alumni {self.first_name} {self.last_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'gender': self.gender,
            'degree': self.degree,
            'department': self.department,
            'graduation_year': self.graduation_year,
            'student_id': self.student_id,
            'current_employer': self.current_employer,
            'job_title': self.job_title,
            'industry': self.industry,
            'years_of_experience': self.years_of_experience,
            'linkedin': self.linkedin,
            'current_city': self.current_city,
            'state': self.state,
            'country': self.country,
            'technical_skills': self.technical_skills,
            'languages_known': self.languages_known,
            'areas_of_interest': self.areas_of_interest
        } 