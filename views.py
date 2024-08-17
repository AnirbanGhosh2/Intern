from flask import Blueprint,request
from website import get_connection,company_data,enrich_data,store_enriched_data
from flask import jsonify

views=Blueprint('views',__name__)

@views.route('/company',methods=['GET','POST'])
def home():
    if request.method=='GET':
        connection=get_connection()
        data= company_data(connection)
        enriched_data = enrich_data(data)
        if not enriched_data:
            print("No data was enriched. Exiting.")
            return
        store_enriched_data(connection, enriched_data)
        
        print("Data enrichment and storage process completed successfully.")


    

