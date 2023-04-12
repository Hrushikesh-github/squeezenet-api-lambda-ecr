import requests
import base64
import json

url = 'https://ouyn2mmy44.execute-api.us-east-1.amazonaws.com/prod/'

with open("/Users/hrushi/Desktop/squeezenet/parrot.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

payload = {"body": encoded_string}
#headers = {'Content-Type': 'application/json'}

#response = requests.post(url, data=payload, headers=headers)
response = requests.post(url, json=payload)
print(response.status_code)
print(response)
