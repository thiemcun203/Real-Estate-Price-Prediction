# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from google.cloud import firestore
from google.oauth2 import service_account
from house_price_scraper.settings import firebase_key, project_id
import hashlib
from tqdm import tqdm


def generate_unique_id(input_str):
    # Create a SHA-256 hash object
    sha256_object = hashlib.sha256()

    # Update the hash object with the input string encoded as bytes
    sha256_object.update(input_str.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    unique_id = sha256_object.hexdigest()

    return unique_id

class HousePriceScraperPipeline:
    def process_item(self, item, spider):
        return item
    
class FirebasePipeline(object):
    def __init__(self):
        
        # Initialize the app with a service account, granting admin privileges
        self.creds = service_account.Credentials.from_service_account_info(firebase_key)
        self.project_id = project_id
        # Get the database "batdongsan"
        self.database = firestore.Client(credentials=self.creds, project=self.project_id)
        

    def process_item(self, item, spider):
        id  = generate_unique_id(item['url'])
        collection = self.database.collection(u'nhadatvn')
        doc_ref = collection.document(id)
        doc = doc_ref.get()
        if doc.exists:
            spider.logger.warn("Item already in the database: %s" % item['url'])
        else:
            data = {
                u'html_content': item['html_content'],
                u'url': item['url'],
            }
            doc_ref.set(data)
            spider.logger.info('Item saved to database successfully: %s' % item['url'])
        item['progress_bar'].update(1)
        return item

# class ProgressBarPipeline:
    
#     def process_item(self, item, spider):
#         with tqdm(total=len(spider.sub_pages), desc=f"Processing page: {self.num_page}") as pbar:
#             spider.progress_bar = pbar
#             spider.progress_bar.update(1)
#         return item
