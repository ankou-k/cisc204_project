import requests
import json

lettuce = input('Have everyone fill out a lettucemeet if you have not so already.\n The program will scrape the names and availabilities to produce the activity schedule.\nEnter the lettucemeet link here:\n ')

code = lettuce[:-5]

headers = {
    'authority': 'api.lettucemeet.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://lettucemeet.com',
    'referer': 'https://lettucemeet.com/',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

json_data = {
    'id': 'EventQuery',
    'query': 'query EventQuery(\n  $id: ID!\n) {\n  event(id: $id) {\n    ...Event_event\n    ...EditEvent_event\n    id\n  }\n}\n\nfragment EditEvent_event on Event {\n  id\n  title\n  description\n  type\n  pollStartTime\n  pollEndTime\n  maxScheduledDurationMins\n  pollDates\n  isScheduled\n  start\n  end\n  timeZone\n  updatedAt\n}\n\nfragment Event_event on Event {\n  id\n  title\n  description\n  type\n  pollStartTime\n  pollEndTime\n  maxScheduledDurationMins\n  timeZone\n  pollDates\n  start\n  end\n  isScheduled\n  createdAt\n  updatedAt\n  user {\n    id\n  }\n  googleEvents {\n    title\n    start\n    end\n  }\n  pollResponses {\n    id\n    user {\n      __typename\n      ... on AnonymousUser {\n        name\n        email\n      }\n      ... on User {\n        id\n        name\n        email\n      }\n      ... on Node {\n        __isNode: __typename\n        id\n      }\n    }\n    availabilities {\n      start\n      end\n    }\n    event {\n      id\n    }\n  }\n}\n',
    'variables': {
        'id': 'R6lYw',
    },
}
for_df = []
response = requests.post('https://api.lettucemeet.com/graphql', headers=headers, json=json_data)
json = response.json()

jsondata = json["data"]["event"]["pollResponses"]
for i in jsondata:
  a = i["user"]["name"]
  b = i["user"]["email"]
  c = i["availabilities"][0]["start"][0:-8]
  d = i["availabilities"][0]["end"][0:-8]
  for_df.append([a, b, c, d])

df = pd.DataFrame(for_df,columns=[
    "Name",
    "Email",
    "Start Time",
    "End Time"
    ])

print(df)
df.to_csv(f"LettuceMeet.csv")
