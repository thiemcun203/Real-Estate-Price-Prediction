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
collection_ref = database.collection(u'ibatdongsan')                                # ----------> Change this to your desired collection

# ---------- GET NUMBER OF DOCUMENTS ---------- #
query = collection_ref.where(filter=FieldFilter("url", "!=", "0"))
documents = query.stream()
aggregate_query = aggregation.AggregationQuery(query)
num_docs = aggregate_query.count(alias="url").get()[0][0].value

# ---------- CONSTANTS ---------- #
PATTERN = r'^\s*([-+]?\d*\.?\d+)\s+(.*)$'
OUTPUT_PATH = 'house_price_eda/extracted_data_ibatdongsan_0.json'                   # ----------> Change this to your desired output path
LOG_FILE_PATH = 'get_data_ibatdongsan.log'                                          # ----------> Change this to your desired log file path

# ---------- EXTRACT DATA ---------- #
last_processed_identifier = ''                                                      # ----------> If error, change this to the url of the last processed document
idx_offset = 0                                                                      # ----------> If error, change this to the index of the last processed document (see log file) + 1. Then re-run.
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)

for batch_idx in range((num_docs - idx_offset) // 200 + 1):                         
    documents = collection_ref.order_by('url').start_after({
        'url': last_processed_identifier
        }).stream()

    for doc_idx, document in enumerate(documents):                                  # ----------> Change (1)-(4) to fit the logic of your scraper. (0), (5)-(7) can be kept the same.               
        
        # Dealing with documents from the wrong webpage (40 first docs) 
        # NOTE: only if you start from the beginning
        # if batch_idx == 0 and doc_idx <= 39:
        #     continue

        # (0) ---------- SETTING UP ---------- #
        doc = document.to_dict()
        logging.info(f"{batch_idx*200 + doc_idx + idx_offset} {doc['url']}")
        
        url = document.to_dict()['url']
        html = document.to_dict()['html_content']
        sel = Selector(text=html)
        house_info = {}

        # (1) ---------- EXTRACT LOCATION ---------- #
        try:
            house_info['Địa chỉ'] = sel.css('div.address > span.value::text').extract_first().lstrip().rstrip()
        except:
            pass

        # (2) ---------- EXTRACT MAIN INFORMATION ---------- #
        all_texts = sel.css('div.moreinfor1 > div.infor ::text').extract()
        all_labels = ['Ngày đăng', 'Mã tin', 'Hướng', 'Phòng ăn', 
                      'Loại tin', 'Lộ giới', 'Nhà bếp', 
                      'Loại BDS', 'Pháp lý', 'Sân thượng',
                      'Chiều ngang', 'Số lầu', 'Chỗ để xe hơi',
                      'Chiều dài', 'Số phòng ngủ', 'Chính chủ',
                      'Diện tích', 'Giá']
        idx_of_label = 0
        while True:
            try:
                # ---------- (2.1) EXTRACT AREA ---------- #
                if all_texts[idx_of_label] == 'Diện tích':
                    label = 'Diện tích'
                    unit_label = label + '_unit'
                    raw_value = all_texts[idx_of_label + 1].replace(',', '.') 
                    value, unit = raw_value[:-1], raw_value[-1]
                    house_info[label] = float(value)
                    house_info[unit_label] = unit
                    idx_of_label += 3
                
                # ---------- (2.2) EXTRACT PRICE ---------- #
                elif all_texts[idx_of_label] == 'Giá':
                    label = 'Giá'
                    unit_label = label + '_unit'
                    raw_value = all_texts[idx_of_label + 1].replace(',', '.')
                    value, unit = raw_value.split()
                    value = float(value)
                    house_info[label] = value
                    house_info[unit_label] = unit
                    idx_of_label += 2

                # ---------- (2.3) EXTRACT INFORMATION WITH UNIT ---------- #
                elif all_texts[idx_of_label + 1] not in all_labels and re.match(r'^[\d.,]+m$', all_texts[idx_of_label + 1]):
                    label = all_texts[idx_of_label]
                    unit_label = label + '_unit'
                    raw_value = all_texts[idx_of_label + 1].replace(',', '.')
                    value, unit = raw_value[:-1], raw_value[-1]
                    house_info[label] = float(value)
                    house_info[unit_label] = unit
                    idx_of_label += 2
                
                # ---------- (2.4) EXTRACT INFORMATION WITHOUT UNIT ---------- #
                elif all_texts[idx_of_label + 1] not in all_labels:
                    label = all_texts[idx_of_label]
                    value = all_texts[idx_of_label + 1]
                    house_info[label] = value
                    idx_of_label += 2

                # ---------- (2.5) EXTRACT YES/NO INFORMATION ---------- #
                elif all_texts[idx_of_label + 1] in all_labels:
                    label = all_texts[idx_of_label]
                    house_info[label] = 'Yes'
                    idx_of_label += 1
            except:
                break
        
        # (3) ---------- EXTRACT DESCRIPTION TEXT ---------- #
        try:
            house_info['Mô tả'] = "".join(sel.css('div.detail.text-content::text').extract())
        except:
            pass

        # (5) ---------- LOAD EXISTING DATA INTO JSON FILE ---------- #
        existing_data = []
        try:
            with open(OUTPUT_PATH, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            pass

        # (6) ---------- APPEND & SAVE NEW DATA TO EXISTING DATA ---------- #
        existing_data.append(house_info)
        with open(OUTPUT_PATH, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)
        
        # (7) ---------- UPDATE LAST PROCESSED IDENTIFIER ---------- #
        if doc_idx == 199:
            last_processed_identifier = document.to_dict()['url']
            break
    
    if batch_idx % 5 == 4:
        OUTPUT_PATH = OUTPUT_PATH.replace(str(batch_idx // 5), str(batch_idx // 5 + 1))

    print("Batch extraction (to {0}) completed.".format(batch_idx*200 + doc_idx + idx_offset))