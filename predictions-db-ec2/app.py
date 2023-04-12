def handler(event, context):
    print("INSIDE HANDLER")
    import torch
    print("IMPORTED torch THANK U!")
    import torchvision
    print("Torchvision imported")

    import utils
    import json
    #with open("/Users/hrushi/im/api-image/encoded_image.txt", "rb") as file:
    #    encoded_string = file.read()

    encoded_string = event['body']
    predictions, s3_path = utils.get_inference_result(encoded_string)
    print("THE s3 PATH is: ", s3_path)
    print(predictions)
    utils.upload_predictions(predictions, s3_path)
    print("Now returning")
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"predictions": predictions, "s3_path": s3_path})
    }
    return response

#if __name__ == "__main__":
#    handler(1, 1)