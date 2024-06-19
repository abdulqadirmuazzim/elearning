from django.test import TestCase
import requests

url = "https://temu-com-shopping-api-realtime-api-scrapper-from-temu-com.p.rapidapi.com/details"

querystring = {"goodsId": "601099557952370"}

headers = {
    "x-rapidapi-key": "6330cf2960mshf176ae0a766bfc6p1197b3jsn01a475a1c78d",
    "x-rapidapi-host": "temu-com-shopping-api-realtime-api-scrapper-from-temu-com.p.rapidapi.com",
}

response = requests.get(url, headers=headers, params=querystring)

json = response.json()

# details = json["data"]['details']

# for item in json["data"]:
#     print(item)

print(json)
