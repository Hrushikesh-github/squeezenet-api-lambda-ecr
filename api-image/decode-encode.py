import base64

# Load the image as bytes
with open("/Users/hrushi/Desktop/eagle.jpeg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

# Write the encoded string to a file
with open("encoded_image_eagle.txt", "wb") as file:
    file.write(encoded_string)


'''
# Construct the payload with the encoded image data
payload = {"image": encoded_string.decode("utf-8")}

import base64

# Get the encoded image data from the API response
encoded_string = response.json()["image"]

# Decode the image data and write it to a file
with open("/path/to/image.jpg", "wb") as image_file:
    image_file.write(base64.b64decode(encoded_string))
'''
