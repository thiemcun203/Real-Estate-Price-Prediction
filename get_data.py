import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore
from google.oauth2 import service_account
from house_price_scraper.house_price_scraper.settings import firebase_key, project_id

creds = service_account.Credentials.from_service_account_info(firebase_key)
project_id = project_id
database = firestore.Client(credentials=creds, project=project_id)
collection_ref = database.collection(u'nhadatvn')


# Query documents in the collection
documents = collection_ref.stream()

# ----------------- DATA EXTRACTION ----------------- #

import re
import pandas as pd
from IPython.display import display
from scrapy import Selector
from collections import defaultdict

PATTERN = r'^\s*([-+]?\d*\.?\d+)\s+(.*)$'

house_data = pd.DataFrame()

for idx, document in enumerate(documents):
    if idx == 500:
        break
    url = document.to_dict()['url']
    html = document.to_dict()['html_content']
    sel = Selector(text=html)
    all_texts = sel.css('div.tinbds-row-3 > ul > li ::text').extract()
    
    idx_of_label = 0
    house_info = defaultdict(list)
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
    
    house_info = pd.DataFrame(house_info, index=[0])
    house_data = pd.concat([house_data, house_info], ignore_index=True)

display(house_data)
house_data.to_csv('house_data.csv', index=False)