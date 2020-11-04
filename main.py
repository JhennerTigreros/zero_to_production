import googleapiclient.discovery
import numpy as np
from PIL import Image
import json
import codecs
import time
from google.api_core.client_options import ClientOptions
import argparse

args = argparse.ArgumentParser(
    description='Argumentos para utilizar el modelo desplegado.'
)

args.add_argument("--project-id", dest='project_id', type=str, required=True)
args.add_argument("--img-path", dest='img_path', type=str, required=True)
args.add_argument("--region", dest='region', type=str)
args.add_argument("--model", dest='model', type=str, required=True)
args.add_argument("--version", dest='version', type=str, required=True)
args.add_argument("--class-names", nargs='+', dest='class_names', required=True)

args = args.parse_args()

def predict_json(project, region, model, instances, version=None):
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)
    start = time.time()
    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()
    end = time.time()

    print('Prediction Time: {}'.format(end - start))

    if 'error' in response:
        raise RuntimeError(response['error'])
    return response['predictions']

img = Image.open(args.img_path)
img.load()
img = img.resize((180, 180))
data = np.asarray(img, dtype = 'int32')
data = np.expand_dims(data, axis = 0)

class_names = args.class_names
for i in range(1, 100):
    scores = predict_json(args.project_id, args.region, args.model, data.tolist(), args.version)
    print(scores)
    print(class_names[np.argmax(scores)])