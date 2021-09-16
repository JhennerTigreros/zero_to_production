import googleapiclient.discovery
import numpy as np
from PIL import Image
import json
import time
from google.api_core.client_options import ClientOptions
import argparse
import requests

args = argparse.ArgumentParser(
    description='Argumentos para utilizar el modelo desplegado.'
)

args.add_argument("--img-path", dest='img_path', type=str, required=True)
args.add_argument("--model", dest='model', type=str, required=True)
args.add_argument("--version", dest='version', type=str, required=True)
args.add_argument("--class-names", nargs='+', dest='class_names', required=True)

args = args.parse_args()

def predict_json(model, instances, version=None):
    payload = json.dumps({
            "instances": instances
        })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", f'http://localhost:8501/v1/models/{model}/versions/{version}:predict', headers=headers, data=payload).json()

    return response['predictions'][0]


img = Image.open(args.img_path)
img.load()
img = img.resize((180, 180))
data = np.asarray(img, dtype = 'int32')
data = np.expand_dims(data, axis = 0)

class_names = args.class_names
for i in range(1, 1000):
    scores = predict_json(args.model, data.tolist(), args.version)
    print(scores)
    print(class_names[np.argmax(scores)])