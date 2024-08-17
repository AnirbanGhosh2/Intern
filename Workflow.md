Overview
The script is designed to extract company data from a SQL database, enrich it with additional information from the LinkedIn Bulk Data Scraper API, and then store the enriched data back into a new table in the same database.

Detailed Workflow
1. Configuration and Imports
Database Configuration (db_config): Specifies the database connection details such as host, user, password, and database.
API Configuration: Contains the LinkedIn API URL (linkedin_api_url) and API key (linkedin_api_key).
Imports: The script imports necessary modules such as mysql.connector for database operations, requests for making API calls, and json for handling JSON data.

2. Database Connection (connect_to_db)
The function connect_to_db() attempts to connect to the specified SQL database using the provided credentials in db_config.
If the connection is successful, it returns the connection object.
If it fails, it prints an error message and returns None.

3. Extracting Company Data (extract_company_data)
This function extracts company data from the database.
It connects to the database using the connection object and runs a SQL query to select company_id and company_url from the companies table.
The result is returned as a list of dictionaries, where each dictionary represents a company with its company_id and company_url.

4. Enriching Data (enrich_data)
Purpose: This function enriches the extracted company data by calling the LinkedIn API to retrieve additional information.
API Request: For each company, the function sends a POST request to the LinkedIn API with the company's URL as the payload. The API returns enriched data, such as the number of followers, company size, and latest news.
Handling Rate Limits: If the API responds with a 429 status code (indicating too many requests), the script waits for 60 seconds before retrying. This prevents hitting the API rate limit.
Invalid API Key: If the API responds with a 401 status code (indicating an invalid API key), the script will not retry, and the company data will not be enriched.
Data Enrichment: The enriched data is appended to a list which is later used to update the database.

5. Storing Enriched Data (store_enriched_data)
Create Table: The function first checks if the enriched_companies table exists in the database. If it doesn't, it creates the table.
Insert Data: The function inserts the enriched data into this new table. If the company already exists in the table (based on company_id), the existing records are updated with the new information (followers, company size, latest news).

6. Main Workflow (main)
Step 1: Connect to Database: The script first tries to establish a database connection using connect_to_db(). If the connection fails, the script stops.
Step 2: Extract Company Data: The script then extracts the company data from the database using extract_company_data().
Step 3: Enrich Data: The extracted company data is enriched by calling the LinkedIn API using enrich_data().
Step 4: Store Enriched Data: The enriched data is stored in the database using store_enriched_data().
Step 5: Cleanup: The script closes the database connection once all operations are complete.

7. Execution (if __name__ == "__main__": main())
This line ensures that the main() function is executed when the script is run directly.
