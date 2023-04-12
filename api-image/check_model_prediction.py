import base64

# Load the image as bytes
with open("/Users/hrushi/im/ec2_torch_docker/parrot.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

### WE WOULD BE SENDING THE encoded_string to api -> lambda

from PIL import Image
import io
import torch
from torchvision import transforms
import torchvision.models as models


#decoded_image = base64.b64decode(encoded_string)

model_path = '/Users/hrushi/im/ec2_torch_docker/squeezenet_model.pth'
model = models.squeezenet1_1(weights=None)
state_dict = torch.load(model_path)
model.load_state_dict(state_dict)
model.eval()
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.2235]),
])

with open("encoded_image_koyila.txt", "rb") as file:
    encoded_string = file.read()
# Decode the image data
decoded_image = base64.b64decode(encoded_string)
input_image = Image.open(io.BytesIO(decoded_image))
input_tensor = preprocess(input_image)
input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

with torch.no_grad():
    output = model(input_batch)

# Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
#print(output[0])

# The output has unnormalized scores. To get probabilities, you can run a softmax on it.
probabilities = torch.nn.functional.softmax(output[0], dim=0)
#print(probabilities)

with open("/Users/hrushi/im/ec2_torch_docker/imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]
# Show top categories per image
top5_prob, top5_catid = torch.topk(probabilities, 5)
result = []
for i in range(top5_prob.size(0)):
    print(categories[top5_catid[i]], top5_prob[i].item())
    result.append((i+1, categories[top5_catid[i]], round(top5_prob[i].item() * 100, 1)))

print(result)