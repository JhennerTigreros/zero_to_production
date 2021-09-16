FROM tensorflow/serving

RUN apt-get update && apt-get install curl -y

COPY ./flowers /models/flowers