import requests
from pprint import pprint
from config import token, database_id

url = f"https://api.notion.com/v1/databases/{database_id}/query"

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json",
    "Notion-Version": "2022-06-28"}

payload = {
           "filter": {
               "property": "Date",
               "date": {
                   "after": "2023-06-15"
               }
           }
        }


response = requests.post(url, json=payload, headers=headers).json()

print(len(response))
pprint(response)
