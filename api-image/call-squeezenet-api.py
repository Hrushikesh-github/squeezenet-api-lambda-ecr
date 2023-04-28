import requests
import base64
from PIL import Image
import io

# Load the image file and encode it in base64
with open("/Users/hrushi/Desktop/squeezenet/parrot.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
url = 'https://jdfvwltwu2.execute-api.us-east-1.amazonaws.com/develop'
with open("/Users/hrushi/Desktop/eagle.jpeg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

headers = {'Content-Type': 'application/octet-stream'}
response = requests.post(url, data=encoded_string, headers=headers)

print(response.text)

# Print the response
#print(response.text)
