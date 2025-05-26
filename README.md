# Alumni Management System

A web-based Alumni Management System built with Python Flask, MySQL, and HTML/CSS.

## Features
- Alumni List View
- Alumni Profile View
- Add/Edit Alumni Information
- Dashboard with Statistics

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MySQL database:
- Create a database named 'alumni_db'
- Update database credentials in config.py

3. Run the application:
```bash
python app.py
```

4. Access the application at http://localhost:5000

## Project Structure
- `app.py`: Main application file
- `config.py`: Database configuration
- `static/`: CSS and static files
- `templates/`: HTML templates
- `models.py`: Database models 