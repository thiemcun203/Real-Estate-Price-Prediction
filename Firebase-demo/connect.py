# pip install firebase_admin
# more infor: https://cloud.google.com/firestore/docs/manage-data/add-data#python
from google.cloud import firestore
from google.oauth2 import service_account
import json


def connect_firebase(project_id :str):
    # Get the service account key JSON file contents
    with open("/Users/nguyenbathiem/Coding/Semester V/DE/Scrapy/Firebase-demo/firebase-key.json") as key_file:
        firebase_key = json.load(key_file) 

    # Initialize the app with a service account, granting admin privileges
    print(type(firebase_key))
    creds = service_account.Credentials.from_service_account_info(firebase_key)
    # Get the database "batdongsan"
    database = firestore.Client(credentials=creds, project=project_id)

    return database

if __name__ == "__main__":
    db = connect_firebase('house-price-prediction-20231')
    collection_name = 'batdongsan-demo'
    collection = db.collection(collection_name)
    new_row = {'data': 'html_content'}
    
    #add new row, each collection is table, each row is document
    update_time, data_ref = collection.add(new_row)
    print(f"Added document with id {data_ref.id}")
    
    #add with id
    id = '1'
    collection.document(id).set(new_row)
    
    #get data with id
    doc_ref = collection.document(id)
    doc = doc_ref.get()
    html_string = doc.to_dict()['data']
    print(html_string)
