import requests
import base64

url = 'https://ty4wnijtsg.execute-api.us-east-1.amazonaws.com/devy'

with open("/Users/hrushi/Desktop/squeezenet/parrot.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

payload = {"body": encoded_string}
#headers = {'Content-Type': 'application/json'}
#response = requests.post(url, data=payload, headers=headers)
response = requests.post(url, json=payload)
print(response.status_code)
print(response)
response_text = response.text
print(response_text)
response_headers = response.headers
print(response_headers)
print('*' * 20)
print(response.content)

