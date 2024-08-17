from flask import Flask
import mysql.connector
import requests
import json
from flask import Flask
import time

db_config = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12726188',
    'password': 'z2SGNJpjjt',
    'database': 'sql12726188'
}

linkedin_url="https://linkedin-bulk-data-scraper.p.rapidapi.com/person_data_with_educations"
x_rapidapi_key="a69485680cmsh39a9c3fd8b06dd9p14d93ejsn77f748ec3016"

def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_connection():
    connection = connect_to_db()
    return connection

def company_data(connection):
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT company_id,company_url FROM company_data")
    return cursor.fetchall()
def enrich_data(companies):
    enriched_data = []
    headers = {
        "Authorization": f"Bearer {x_rapidapi_key}",
        "Content-Type": "application/json"
    }
    
    for company in companies:
        payload = json.dumps({
            "link": company['company_url']
        })
        
        while True:  # Retry loop
            response = requests.post(linkedin_url, headers=headers, data=payload)
            
            if response.status_code == 200:
                linkedin_data = response.json()
                enriched_data.append({
                    'company_id': company['company_id'],
                    'company_name': linkedin_data.get('name', 'Unknown'),
                    'linkedin_followers': linkedin_data.get('followers', 0),
                    'company_size': linkedin_data.get('companySize', 'Unknown'),
                    'latest_news': linkedin_data.get('latestNews', 'No news available')
                })
                break
            elif response.status_code == 429:
                print(f"Rate limit hit for {company['company_url']}")
                time.sleep(60) 
            else:
                print(f"Failed to fetch data for {company['company_url']}: {response.status_code} - {response.text}")
                break 
            return enriched_data
def store_enriched_data(connection, enriched_data):
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS enriched_companies (
        company_id INT PRIMARY KEY,
        company_name VARCHAR(255),
        linkedin_followers INT,
        company_size VARCHAR(50),
        latest_news TEXT
    )
    """
    cursor.execute(create_table_query)
    
    insert_query = """
    INSERT INTO enriched_companies (company_id, company_name, linkedin_followers, company_size, latest_news)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    linkedin_followers = VALUES(linkedin_followers),
    company_size = VALUES(company_size),
    latest_news = VALUES(latest_news)
    """
    
    for data in enriched_data:
        cursor.execute(insert_query, (
            data['company_id'], data['company_name'], data['linkedin_followers'], data['company_size'], data['latest_news']
        ))
    
    connection.commit()
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='FERFERFERWFREEFERF EREFRF'
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    

    return app
