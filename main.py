import requests
from pprint import pprint
from config import token, source_database_id, target_database_id
from datetime import date


def get_data():

    url = f"https://api.notion.com/v1/databases/{source_database_id}/query"

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

    return response["results"]


# pprint(get_data())


def create_page_template():
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28"}

    create_page_body = {
        "parent": {"database_id": target_database_id},
        "properties": {
                       "title": {
                                 "title": [{
                                            "type": "text",
                                            "text": {"content": f"{date.today().strftime('%B')} Report"}
                                          }]
                                 }
                       },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                              "rich_text":
                                   [{
                                    "type": "text",
                                    "text": {"content": "Карьера"},
                                    "plain_text": "Карьера"
                                   }],
                              "color": "default"
                              }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": "Блог"},
                            "plain_text": "Карьера"
                        }],
                    "color": "default"
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": "Блог"},
                            "plain_text": "Блог"
                        }],
                    "color": "default"
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": "Саморазвитие"},
                            "plain_text": "Саморазвитие"
                        }],
                    "color": "default"
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": "Красота и здоровье"},
                            "plain_text": "Красота и здоровье"
                        }],
                    "color": "default"
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": "Отдых и отношения"},
                            "plain_text": "Отдых и отношения"
                        }],
                    "color": "default"
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": "Жизнь в порядке"},
                            "plain_text": "Жизнь в порядке"
                        }],
                    "color": "default"
                }
            }
                   ]
                        }

    response = requests.post(url, json=create_page_body, headers=headers).json()

    return response


pprint(create_page_template())
