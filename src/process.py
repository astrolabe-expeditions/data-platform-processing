import os
import requests

import pandas as pd
import boto3
from dotenv import load_dotenv

from main import run
import io
from flask import abort
import json

def connect_to_s3():
  s3 = boto3.client('s3',
    endpoint_url = os.environ['S3_ENDPOINT'],
    config = boto3.session.Config(signature_version = 's3v4'),
    aws_access_key_id = os.environ['S3_ID'],
    aws_secret_access_key = os.environ['S3_SECRET'],
    aws_session_token = None)
  return s3

class PandasEncoder(json.JSONEncoder):
    def default(self, obj):
      if(isinstance(obj, pd._libs.tslibs.timestamps.Timestamp)):
        return str(obj.to_pydatetime())

      return super(PandasEncoder, self).default(obj)

def process_file(file_id):
  load_dotenv() # load environment variables from .env file

  # Retrieve the file JSON via the API route
  file_url = f"http://localhost:3000/api/v1/files/{file_id}"
  response = requests.get(file_url)
  if response.status_code == 200:
    file = response.json()['data']
  else:
    file = None

  if file is None:
    abort(404, description="Resource not found")

  # Mise à jour du status du fichier à en cours
  print(f"File {file_id} - {file['name']} being processed")
  file["status"] = "in_process"  # Update the status to "in_process"
  update_response = requests.put(file_url, json=file)
  if update_response.status_code != 200:
    # Handle the error if the update fails
    abort(update_response.status_code, description="Failed to update file status")

  # Insertion de lecture et traitement du dataset
  s3 = connect_to_s3()
  Key= "sensors/" + str(file["sensor_id"]) + "/" + file_id + ".csv"
  response = s3.get_object(Bucket=os.environ['S3_BUCKET'], Key = Key)
  content = response['Body'].read().decode('utf-8')
  data = pd.read_csv(io.StringIO(content), delimiter=";")
  dataset = run(data)
  print(f"File {file_id} - cleaned and transformed")

  # Insertion des colonnes manquantes dans le dataset
  dataset["sensor_id"] = str(file["sensor_id"])

  data_dict = dataset.to_dict("records")
  print(f"File {file_id} - inserting {len(data_dict)} records")
  if data_dict:

    # Envoyer par batch de 100
    batch_size = 100
    num_batches = len(data_dict) // batch_size + 1

    for i in range(num_batches):
      start = i * batch_size
      end = (i + 1) * batch_size
      print(f"File {file_id} - inserting batch {i + 1}/{num_batches}")
      batch_data = []
      for data in data_dict[start:end]:
        transformed_data = {
          "sensor_id": data["sensor_id"],
          "recorded_at": data["recorded_at"],
          "latitude": data["latitude"],
          "longitude": data["longitude"],
          "properties": {
            key: value for key, value in data.items() if key not in ["sensor_id", "recorded_at", "latitude", "longitude"]
          }
        }
        batch_data.append(transformed_data)
      batch_data_json = json.dumps(batch_data, cls=PandasEncoder)

      response = requests.post(f"http://localhost:3000/api/v1/sensors/{file['sensor_id']}/records/create_or_update_many", json={
        "data": batch_data_json
      })

      if response.status_code != 201:
        # Handle the error if the request fails
        abort(response.status_code, description="Failed to insert data")

  # mise à jour du status du fichier à terminé
  print(f"File {file_id} - processed successfully")
  file["status"] = "processed"  # Update the status to "processed"
  update_response = requests.put(file_url, json=file)
  if update_response.status_code != 200:
    # Handle the error if the update fails
    abort(update_response.status_code, description="Failed to update file status")

  return {"message": "success"}, 201