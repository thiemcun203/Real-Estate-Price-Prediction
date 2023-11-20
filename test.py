import hashlib
from google.cloud import firestore
from google.oauth2 import service_account
from house_price_scraper.house_price_scraper.settings import firebase_key, project_id
from bs4 import BeautifulSoup

def generate_unique_id(input_str):
    # Create a SHA-256 hash object
    sha256_object = hashlib.sha256()

    # Update the hash object with the input string encoded as bytes
    sha256_object.update(input_str.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    unique_id = sha256_object.hexdigest()

    return unique_id

# # Example usage
# url = 'https://nhadatvn.com.vn/ban-dat-mat-pho-nguyen-hong-110m2-mat-tien-75m-ngay-nga-tu-kinh-doanh-cho-thue-tot.bds'
url = 'https://nhadatvn.com.vn/0904688633-ban-nha-chua-lang-dong-da-50m2-4t-35-ty-xac-dinh-ban-dat-tang-nha.bds'
url_id = generate_unique_id(url)
print(url_id)

creds = service_account.Credentials.from_service_account_info(firebase_key)
project_id = project_id
database = firestore.Client(credentials=creds, project=project_id)


collection = database.collection(u'nhadatvn')
doc = collection.document(url_id).get()
html_string = doc.to_dict()['html_content']
soup = BeautifulSoup(html_string, 'html.parser')

with open('../output.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print('Done')
    
    
# import pandas as pd
# Read CSV file
# csv_file_path = '/Users/nguyenbathiem/Coding/Semester V/Data Science/Real-Estate-Price-Prediction/nhadatvn.csv'
# df = pd.read_csv(csv_file_path)

# # Access row 1, column 1 (assuming 0-based indexing)
# cell_value = df.iloc[0, 0]

# # Create an HTML file and write the cell value to it
# html_file_path = 'output.html'
# with open(html_file_path, 'w') as html_file:
#     html_file.write(cell_value)

# print(f"Cell value from row 1, column 1 saved to {html_file_path}")


