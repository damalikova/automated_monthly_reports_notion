import requests
from pprint import pprint
from config import token, database_id

url = f"https://api.notion.com/v1/databases/{database_id}/query"

headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json",
            "Notion-Version": "2022-06-28"
          }

payload = {'filter': {'and':
                      [
                        {'date':
                         {'after': '2023-05-31'},
                         'property': 'Date'},
                        {'date':
                         {'before': '2023-07-01'},
                         'property': 'Date'}
                      ]
                      },
           "sorts": [
               {
                   "property": "Date",
                   "direction": "ascending"}
           ]
           }

response = requests.post(url, json=payload, headers=headers).json()

pprint((response["results"][0]))
# pprint(response["results"])
