import re
import json
from scrapy import Selector
from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import service_account
from house_price_scraper.house_price_scraper.settings import firebase_key, project_id

# Query documents in the collection
# query = collection_ref.where(filter=FieldFilter("url", "!=", "0"))
# documents = query.stream()

# # Build the aggregation query
# aggregate_query = aggregation.AggregationQuery(query)

# # Count the documents
# aggregate_query.count(alias="url")

# # Get the results
# results = aggregate_query.get()

# print(f"Number of documents: {results[0][0].value}")
# Initialize Firebase

creds = service_account.Credentials.from_service_account_info(firebase_key)
project_id = project_id
database = firestore.Client(credentials=creds, project=project_id)
collection_ref = database.collection(u'nhadatvn')               # ---------------------------> Change this to your desired collection
documents = collection_ref.stream()

PATTERN = r'^\s*([-+]?\d*\.?\d+)\s+(.*)$'
OUTPUT_PATH = 'house_price_eda/extracted_data_nhadatvn.json'    # ---------------------------> Change this to your desired output path

for idx, document in enumerate(documents):                      # ---------------------------> Change this to fit the logic of your scraper                 
    doc = document.to_dict()
    print(idx, doc['url'])
    
    # if idx == 200:                                            # ---------------------------> Uncomment to test on a small number of documents
    #     break                                                 # ---------------------------> Comment to run on all documents
    
    url = document.to_dict()['url']
    html = document.to_dict()['html_content']
    sel = Selector(text=html)
    house_info = {}

    # (1) ---------- EXTRACT NUMBER OF BEDROOMS ---------- #
    try:
        house_info['Số phòng ngủ'] = int(sel.css('ul.ul_thuoctinhcoban_user > li:nth-child(3)::text').extract()[1].split()[0])
    except:
        pass
    
    # (2) ---------- EXTRACT MAIN INFORMATION ---------- #
    all_texts = sel.css('div.tinbds-row-3 > ul > li ::text').extract()
    idx_of_label = 0
    while True:
        try:
            # ---------- EXTRACT LABEL AND VALUE ---------- #
            label = all_texts[idx_of_label].lstrip()
            value = all_texts[idx_of_label + 1]
            unit_label = None
            unit = None
            
            # ---------- EXTRACT UNIT IF NEEDED ---------- #
            if re.match(PATTERN, value):
                unit_label = label + "_unit"
                value, unit = all_texts[idx_of_label + 1].split()
                if value.isdigit():
                    value = int(value)
                else:
                    value = float(value)
            
            # ---------- UPDATE INDEX OF LABEL ---------- #
            if label == 'Diện tích':
                idx_of_label += 3
            else:
                idx_of_label += 2

            # ---------- UPDATE INFO DICT ---------- #
            house_info[label] = value
            if unit_label and unit:
                house_info[unit_label] = unit

        except:
            break
    
    # (3) ---------- EXTRACT DATE OF UPLOAD ---------- #
    try:
        house_info['Ngày đăng'] = sel.css('ul.ul_thoihandangtin > li:nth-child(1)::text').extract()[1].rstrip().lstrip()
        house_info['Ngày hết hạn'] = sel.css('ul.ul_thoihandangtin > li:nth-child(2)::text').extract()[1].rstrip().lstrip()
    except:
        pass
    
    # Load existing data from the JSON file
    existing_data = []
    try:
        with open(OUTPUT_PATH, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        pass  # The file might not exist yet, which is okay

    # Append the new data to the existing data
    existing_data.append(house_info)

    # Save the combined data to the JSON file
    with open(OUTPUT_PATH, 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)

print("Extraction completed.")
