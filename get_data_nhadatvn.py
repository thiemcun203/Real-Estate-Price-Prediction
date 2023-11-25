import re
import json
import logging
from scrapy import Selector
from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import service_account
from house_price_scraper.house_price_scraper.settings import firebase_key, project_id

# ---------- INITIALIZE FIRESTORE CLIENT ---------- #
creds = service_account.Credentials.from_service_account_info(firebase_key)
project_id = project_id
database = firestore.Client(credentials=creds, project=project_id)
collection_ref = database.collection(u'nhadatvn')                                   # ----------> Change this to your desired collection

# ---------- GET NUMBER OF DOCUMENTS ---------- #
query = collection_ref.where(filter=FieldFilter("url", "!=", "0"))
documents = query.stream()
aggregate_query = aggregation.AggregationQuery(query)
num_docs = aggregate_query.count(alias="url").get()[0][0].value

# ---------- CONSTANTS ---------- #
PATTERN = r'^\s*([-+]?\d*\.?\d+)\s+(.*)$'
OUTPUT_PATH = 'house_price_eda/extracted_data_nhadatvn_2.json'                        # ----------> Change this to your desired output path
LOG_FILE_PATH = 'get_data_nhadatvn.log'                                             # ----------> Change this to your desired log file path

# ---------- EXTRACT DATA ---------- #
last_processed_identifier = ''                                                      # ----------> If error, change this to the url of the last processed document
idx_offset = 0                                                                      # ----------> If error, change this to the index of the last processed document (see log file) + 1. Then re-run.
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)

for batch_idx in range((num_docs - idx_offset) // 200 + 1):                         
    documents = collection_ref.order_by('url').start_after({
        'url': last_processed_identifier
        }).stream()

    for doc_idx, document in enumerate(documents):                                  # ----------> Change (1)-(3) to fit the logic of your scraper. (0), (4)-(6) can be kept the same.               
        
        # (0) ---------- SETTING UP ---------- #
        doc = document.to_dict()
        logging.info(f"{batch_idx*200 + doc_idx + idx_offset} {doc['url']}")
        
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
                # ---------- (2.1) EXTRACT LABEL AND VALUE ---------- #
                label = all_texts[idx_of_label].lstrip()
                value = all_texts[idx_of_label + 1]
                unit_label = None
                unit = None
                
                # ---------- (2.2) EXTRACT UNIT IF NEEDED ---------- #
                if re.match(PATTERN, value):
                    unit_label = label + "_unit"
                    value, unit = all_texts[idx_of_label + 1].split()
                    if value.isdigit():
                        value = int(value)
                    else:
                        value = float(value)
                
                # ---------- (2.3) UPDATE INDEX OF LABEL ---------- #
                if label == 'Diện tích':
                    idx_of_label += 3
                else:
                    idx_of_label += 2

                # ---------- (2.4) UPDATE INFO DICT ---------- #
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
        
        # (4) ---------- LOAD EXISTING DATA INTO JSON FILE ---------- #
        existing_data = []
        try:
            with open(OUTPUT_PATH, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            pass

        # (5) ---------- APPEND & SAVE NEW DATA TO EXISTING DATA ---------- #
        existing_data.append(house_info)
        with open(OUTPUT_PATH, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)
        
        # (6) ---------- UPDATE LAST PROCESSED IDENTIFIER ---------- #
        if doc_idx == 199:
            last_processed_identifier = document.to_dict()['url']
            break

    print("Batch extraction completed.")