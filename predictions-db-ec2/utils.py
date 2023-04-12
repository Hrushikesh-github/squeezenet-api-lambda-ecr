import torch
from torchvision import transforms
import torchvision.models as models
import base64
from PIL import Image
import io
import os
import random
import boto3

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text


def get_inference_result(encoded_string):
    model_path = 'model/squeezenet_model.pth'
    model = models.squeezenet1_1(weights=None)
    state_dict = torch.load(model_path)
    model.load_state_dict(state_dict)
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    decoded_image = base64.b64decode(encoded_string)

    # Upload the image to S3
    bucket_name = "hrushikesh-images-storage"
    random_int = random.randint(1, 999)
    s3_key = f'{random_int}.jpg'
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=decoded_image)
    s3_path = os.path.join(bucket_name, s3_key)

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

    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
    # Show top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    result = []
    for i in range(top5_prob.size(0)):
        #print(categories[top5_catid[i]], top5_prob[i].item())
        result.append((i+1, categories[top5_catid[i]], round(top5_prob[i].item() * 100, 1)))

    return result, s3_path

def upload_predictions(result, s3_path='some_path'):
    
    # Configuration values for the RDS instance
    host = 'database-1.c0kpxltmifsg.us-east-1.rds.amazonaws.com'
    port = 5432
    username = 'postgres'
    password = 'shukhapriya'
    database = 'image_predictions'

    
    engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (username, password, host, port, database))
    conn = engine.connect()
    trans = conn.begin()

    print("CONNECTED TO RDS and began a session")
    query = 'SELECT id,image_class,image_url FROM predictions'
    query_result = conn.execute(text(query)).fetchall()
    print('The INITIAL Query result is:', '\n', query_result)

    query = """
    INSERT INTO predictions (upload_method, image_url, prediction1_class, confidence1, prediction2_class, confidence2, prediction3_class, confidence3, prediction4_class, confidence4, prediction5_class, confidence5)
    VALUES (:upload_method, :image_url, :prediction1_class, :confidence1, :prediction2_class, :confidence2, :prediction3_class, :confidence3, :prediction4_class, :confidence4, :prediction5_class, :confidence5)
    """

    values = {
        "upload_method": "local_test",
        "image_url": s3_path,
        "prediction1_class": result[0][1],
        "confidence1": result[0][2],
        "prediction2_class": result[1][1],
        "confidence2": result[1][2],
        "prediction3_class": result[2][1],
        "confidence3": result[2][2],
        "prediction4_class": result[3][1],
        "confidence4": result[3][2],
        "prediction5_class": result[4][1],
        "confidence5": result[4][2]
    }
    conn.execute(text(query), values)
    query = 'SELECT id,image_class,image_url FROM predictions'
    query_result = conn.execute(text(query)).fetchall()
    print('The FINAL Query result is:', '\n', query_result)
    trans.commit()
    conn.close()
    print("EXECUTED SUCCESSFULLY, CLOSING CONNECTION")
    return 1

if __name__ == "__main__":
    print("Y")