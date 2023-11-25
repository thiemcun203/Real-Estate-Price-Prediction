import re
import json
from scrapy import Selector
from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import service_account
from house_price_scraper.house_price_scraper.settings import firebase_key, project_id

# Query documents in the collection

# Initialize Firebase
creds = service_account.Credentials.from_service_account_info(firebase_key)
project_id = project_id
database = firestore.Client(credentials=creds, project=project_id)
collection_ref = database.collection(u'alonhadatvn')
# documents = collection_ref.stream()

query = collection_ref.where(filter=FieldFilter("url", "!=", "0"))
documents = query.stream()

# Build the aggregation query
aggregate_query = aggregation.AggregationQuery(query)

# Count the documents
aggregate_query.count(alias="url")

# Get the results
results = aggregate_query.get()

print(f"Number of documents: {results[0][0].value}")

# PATTERN = r'^\s*([-+]?\d*\.?\d+)\s+(.*)$'

# # Path to the JSON file
# output_file_path = 'extracted_data.json'

# for idx, document in enumerate(documents):
#     doc = document.to_dict()
#     print(idx, doc['url'])
    
#     if idx == 500:
#         break
    
#     url = document.to_dict()['url']
#     html = document.to_dict()['html_content']
#     sel = Selector(text=html)
#     all_texts = sel.css('div.tinbds-row-3 > ul > li ::text').extract()
    
#     idx_of_label = 0
#     house_info = {}

#     while True:
#         try:
#             # ---------- EXTRACT LABEL AND VALUE ---------- #
#             label = all_texts[idx_of_label].lstrip()
#             value = all_texts[idx_of_label + 1]
#             unit_label = None
#             unit = None
            
#             # ---------- EXTRACT UNIT IF NEEDED ---------- #
#             if re.match(PATTERN, value):
#                 unit_label = label + "_unit"
#                 value, unit = all_texts[idx_of_label + 1].split()
#                 if value.isdigit():
#                     value = int(value)
#                 else:
#                     value = float(value)
            
#             # ---------- UPDATE INDEX OF LABEL ---------- #
#             if label == 'Diện tích':
#                 idx_of_label += 3
#             else:
#                 idx_of_label += 2

#             # ---------- UPDATE INFO DICT ---------- #
#             house_info[label] = value
#             if unit_label and unit:
#                 house_info[unit_label] = unit

#         except:
#             break
    
#     # Load existing data from the JSON file
#     existing_data = []
#     try:
#         with open(output_file_path, 'r') as json_file:
#             existing_data = json.load(json_file)
#     except FileNotFoundError:
#         pass  # The file might not exist yet, which is okay

#     # Append the new data to the existing data
#     existing_data.append(house_info)

#     # Save the combined data to the JSON file
#     with open(output_file_path, 'w') as json_file:
#         json.dump(existing_data, json_file, indent=2)

# print("Extraction completed.")
