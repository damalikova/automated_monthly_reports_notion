import requests
from pprint import pprint
from config import token, source_database_id, target_database_id
from datetime import date


def get_data():

    response = []
    weeks = (("2023-06-04", "2023-06-12"), ("2023-06-11", "2023-06-19"), ("2023-06-18", "2023-06-26"), ("2023-06-25", "2023-07-01"))

    for week in weeks:

        url = f"https://api.notion.com/v1/databases/{source_database_id}/query"

        headers = {
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Notion-Version": "2022-06-28"
              }

        payload = {'filter': {
                          "and":
                                [
                                 {
                                  "property": "Date",
                                  "date": {"after": week[0]}
                                 },
                                 {
                                   "property": "Date",
                                   "date": {"before": week[1]}
                                 },
                                 ]
                          },
               "sorts": [

                {
                       "property": "Date",
                       "direction": "ascending"}
            ]
           }

        response.extend(requests.post(url, json=payload, headers=headers).json()["results"])

    return response


def categorize(tasks):
    categorized = dict()

    for task in tasks:

        category = task["properties"]["Категория"]["multi_select"][0]["name"]
        name = task["properties"]["Name"]["title"][0]["plain_text"]

        if category not in categorized:
            categorized[category] = {name: 1}
        else:
            if name in categorized[category]:
                categorized[category][name] += 1
            else:
                categorized[category][name] = 1

    return categorized


def create_report(prepared_data):

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28"}

    children = []

    for category in prepared_data:
        category_json = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text":
                        [{
                            "type": "text",
                            "text": {"content": f"{category}"},
                            "plain_text": f"{category}"
                        }],
                    "color": "default"
                }
            }
        ]
        for task in prepared_data[category].items():

            task_json = {
                                "object": "block",
                                "type": "bulleted_list_item",
                                "bulleted_list_item":
                                                    {
                                                      "rich_text": [{
                                                                     "type": "text",
                                                                     "text": {"content": f"{task[0]} — {task[1]}"}
                                                                    }]
                                                     }
                            }
            category_json.append(task_json)

        children.extend(category_json)

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
        "children": children
                        }

    response = requests.post("https://api.notion.com/v1/pages", json=create_page_body, headers=headers).json()

    return response


pprint(create_report(categorize(get_data())))
