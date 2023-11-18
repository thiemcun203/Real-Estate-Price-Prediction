# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import hashlib

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
        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import firestore
        cred = credentials.Certificate('house-price-scraper-firebase-adminsdk-5k9y7-2b6f7a4a4f.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def process_item(self, item, spider):
        self.db.collection(u'nhadatvn').add(dict(item))
        return item
