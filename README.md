# An API to get image predictions from ImageNet model

## Architecture Design
![image](https://github.com/Hrushikesh-github/squeezenet-api-lambda-ecr/assets/56476887/cf6bf99d-d7ef-4ed4-8c03-cd7a110f4812)

The API was developed to be used in my website, however instead of API I'm moving over to the Microservice architecture. 

#### Steps involved:

1. Send a base64 encoded image as input to API.
2. API which was made in AWS-API-Gateway triggers lambda function
3. Lambda function was created with a ECR container image installed with torch and other required libraries
4. Function gives a prediction as output
5. Function also saves the image into S3 bucket.
6. Function also saves the predictions, S3 path of image into a RDS Postgres Database
7. Finally API returns the predictions
 

### Few Technicalities
1. Container image was created using an EC2 instance as my M1 chip Mac has issues with torch and tensorflow. Even buildx couldn't handle the different architecure conversion. [This is an open problem as of now](https://github.com/tensorflow/serving/issues/1816).
2. Using a lambda function saves lot of costs instead of having the api in an virtual machine
3. To use the lambda function we must use an ECR container due to restrictions in memory size of zip based approach to create lambda function. Increasing lambda memory size to 1200MB worked comfortably for me.
4. I have listed down all the commands and errors I faced in multiple attempts of creating the container image. You can find the doc here [ECR repo creation](https://github.com/Hrushikesh-github/squeezenet-api-lambda-ecr/blob/develop/ECR%20repo%20creation.pdf)
5. Similarly other docs are [AWS Lambda - RDS connection](https://github.com/Hrushikesh-github/squeezenet-api-lambda-ecr/blob/develop/AWS%20Lambda%20and%20RDS%20connection.pdf) and a short introduction for my own understanding of what are [APIs and Web Services](https://github.com/Hrushikesh-github/squeezenet-api-lambda-ecr/blob/develop/API%20and%20Web%20Service%20Introduction.pdf). You might have to download them as github doesn't render inline code.
6. Squeezenet was used because of exceptional low memory of 4.8MB and good performance. Compare this with VGG16 of 270MB and ResNet with 550MB.


### Contents in the repo
There are two directories 
1. [api-image](https://github.com/Hrushikesh-github/squeezenet-api-lambda-ecr/tree/develop/api-image) contains code on how to call the API and few example files. 
2. [ecr-repo-creation](https://github.com/Hrushikesh-github/squeezenet-api-lambda-ecr/tree/develop/predictions-db-ec2) contains code that was used to build the ecr repo.

I would be changing the endpoint credentials to avoid any misuse and save the costs.
Feel free to contact me for more information
