from connect import connect_firebase
import requests
from bs4 import BeautifulSoup

#Connect to firebase
database = connect_firebase('house-price-prediction-20231')
collection_name = 'batdongsan-demo'
collection = database.collection(collection_name)

#Crawl data
url = f'https://nhadatvn.com.vn/nha-dat-ban-kv-ha-noi.html'  # Replace with the actual URL you want to scrape

headers = {
  'authority': 'alonhadat.com.vn',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'ASP.NET_SessionId=vs5kjw55ltbohmf4fk0boq23; ignoredmember=; _gcl_au=1.1.1622563677.1699524562; _ga_ERYH5XEJQM=GS1.1.1699524562.1.0.1699524562.60.0.0; _ga=GA1.1.297262430.1699524562',
  'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55'
}
# Send an HTTP GET request to the URL
response = requests.get(url,
                        headers=headers,
)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    id = 1
    row = {'data': response.text}
    #add new row, each collection is table, each row is document
    collection.document(str(id)).set(row)
    print(f"Added document successfully to firebase with id {id}")

else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

# Parse the HTML content of the page from firebase using BeautifulSoup
doc = collection.document(str(id)).get()
html_string = doc.to_dict()['data']

soup = BeautifulSoup(html_string, 'html.parser')

with open('/Users/nguyenbathiem/Coding/Semester V/DE/Scrapy/Firebase-demo/demo.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
#....doing something with soup: Extract data, etc.
