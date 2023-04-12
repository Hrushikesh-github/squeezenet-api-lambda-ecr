FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y gcc-c++ python3-devel
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install Pillow
RUN pip3 install sqlalchemy psycopg2-binary

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT} 
COPY imagenet_classes.txt ${LAMBDA_TASK_ROOT}
COPY model/ ${LAMBDA_TASK_ROOT}/model/

CMD [ "app.handler" ]
