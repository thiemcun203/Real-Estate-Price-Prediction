# import hashlib

# def generate_unique_id(input_str):
#     # Create a SHA-256 hash object
#     sha256_object = hashlib.sha256()

#     # Update the hash object with the input string encoded as bytes
#     sha256_object.update(input_str.encode('utf-8'))

#     # Get the hexadecimal representation of the hash
#     unique_id = sha256_object.hexdigest()

#     return unique_id

# # Example usage
# url = "https://nhadatvn.com.vn/ban-nhanh-nha-3-tang-biet-thu-tai-phu-thuong-tay-ho-ha-noi-dt-204m-xay-70m-x-3-tang-gara-con-lai-la-san.bds"
# url_id = generate_unique_id(url)
# print(url_id)
import pandas as pd

# Read CSV file
csv_file_path = '/Users/nguyenbathiem/Coding/Semester V/Data Science/Real-Estate-Price-Prediction/nhadatvn.csv'
df = pd.read_csv(csv_file_path)

# Access row 1, column 1 (assuming 0-based indexing)
cell_value = df.iloc[0, 0]

# Create an HTML file and write the cell value to it
html_file_path = 'output.html'
with open(html_file_path, 'w') as html_file:
    html_file.write(cell_value)

print(f"Cell value from row 1, column 1 saved to {html_file_path}")

if [1]: print("hello")
