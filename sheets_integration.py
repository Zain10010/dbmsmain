from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from datetime import datetime
from models import Alumni, db

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1P7v-jaxBcLzeaVmkdjXtu1iRgAHuyUPhD_TjNrZE_UI'
RANGE_NAME = 'Sheet1!A2:Z'  # Adjust range as needed

def get_google_sheets_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def fetch_and_update_alumni():
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return
        
        for row in values:
            try:
                # Check if alumni already exists by email
                existing_alumni = Alumni.query.filter_by(email=row[2]).first()
                
                if existing_alumni:
                    # Update existing alumni
                    existing_alumni.first_name = row[0]
                    existing_alumni.last_name = row[1]
                    existing_alumni.phone = row[3] if len(row) > 3 else ''
                    existing_alumni.degree = row[4] if len(row) > 4 else ''
                    existing_alumni.department = row[5] if len(row) > 5 else ''
                    existing_alumni.graduation_year = int(row[6]) if len(row) > 6 and row[6].isdigit() else None
                    existing_alumni.student_id = row[7] if len(row) > 7 else ''
                    existing_alumni.current_employer = row[8] if len(row) > 8 else ''
                    existing_alumni.job_title = row[9] if len(row) > 9 else ''
                    existing_alumni.industry = row[10] if len(row) > 10 else ''
                    existing_alumni.current_city = row[11] if len(row) > 11 else ''
                    existing_alumni.state = row[12] if len(row) > 12 else ''
                    existing_alumni.country = row[13] if len(row) > 13 else ''
                    existing_alumni.technical_skills = row[14] if len(row) > 14 else ''
                    existing_alumni.languages_known = row[15] if len(row) > 15 else ''
                    existing_alumni.areas_of_interest = row[16] if len(row) > 16 else ''
                else:
                    # Create new alumni
                    new_alumni = Alumni(
                        first_name=row[0],
                        last_name=row[1],
                        email=row[2],
                        phone=row[3] if len(row) > 3 else '',
                        degree=row[4] if len(row) > 4 else '',
                        department=row[5] if len(row) > 5 else '',
                        graduation_year=int(row[6]) if len(row) > 6 and row[6].isdigit() else None,
                        student_id=row[7] if len(row) > 7 else '',
                        current_employer=row[8] if len(row) > 8 else '',
                        job_title=row[9] if len(row) > 9 else '',
                        industry=row[10] if len(row) > 10 else '',
                        current_city=row[11] if len(row) > 11 else '',
                        state=row[12] if len(row) > 12 else '',
                        country=row[13] if len(row) > 13 else '',
                        technical_skills=row[14] if len(row) > 14 else '',
                        languages_known=row[15] if len(row) > 15 else '',
                        areas_of_interest=row[16] if len(row) > 16 else ''
                    )
                    db.session.add(new_alumni)
                
                db.session.commit()
                print(f"Successfully processed alumni: {row[0]} {row[1]}")
                
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {str(e)}")
                db.session.rollback()
                continue
                
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {str(e)}")
        return False
    
    return True 