import hashlib
from google.cloud import firestore
from google.oauth2 import service_account
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
from house_price_scraper.house_price_scraper.settings import firebase_key, project_id
from bs4 import BeautifulSoup
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
import re

def generate_unique_id(input_str, spider_name):
    
    if spider_name == 'nhadatvnSpider':
        input_str = input_str
    elif spider_name == 'ibatdongsanSpider':
        PATTERN = r'[-]+[0-9]+\.html$'
        input_str = re.sub(PATTERN, '', input_str)
    elif spider_name == 'alonhadatvnSpider':
        PATTERN = r'[-]+[0-9]+\.html$'
        input_str = re.sub(PATTERN, '', input_str)
    print(input_str)
    
    # Create a SHA-256 hash object
    sha256_object = hashlib.sha256()

    # Update the hash object with the input string encoded as bytes
    sha256_object.update(input_str.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    unique_id = sha256_object.hexdigest()

    return unique_id

# # Example usage
# spidername = 'alonhadatvnSpider'
spidername = 'ibatdongsanSpider'
# spidername = 'nhadatvnSpider'
# url = 'https://nhadatvn.com.vn/ban-dat-mat-pho-nguyen-hong-110m2-mat-tien-75m-ngay-nga-tu-kinh-doanh-cho-thue-tot.bds'
# url = 'https://alonhadat.com.vn/dat-re-gia-tot-chi-70tr-m2-cho-manh-dat-115m2-o-lac-long-quan-13728976.html'
url = 'https://i-batdongsan.com/ban-nha-pho-pham-ngoc-thach-dong-da-o-to-do-cua-nha-dep-o-ngay-40m2-gia-6-9-ty-4999203.html'
url_id = generate_unique_id(url, spidername)
print(url_id)

creds = service_account.Credentials.from_service_account_info(firebase_key)
project_id = project_id
database = firestore.Client(credentials=creds, project=project_id)

collection = database.collection(spidername[:-6])
try:
    doc = collection.document(url_id).get()
    html_string = doc.to_dict()['html_content']
    soup = BeautifulSoup(html_string, 'html.parser')

    with open('test/output.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print('Done')
except:
    print('Not found')

# Query documents in the collection
query = collection.where(filter=FieldFilter("url", "!=", "0"))
documents = query.stream()

# Build the aggregation query
aggregate_query = aggregation.AggregationQuery(query)

# Count the documents
aggregate_query.count(alias="url")

# Get the results
results = aggregate_query.get()

print(f"Number of documents: {results[0][0].value}")
