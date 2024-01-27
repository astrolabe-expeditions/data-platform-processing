import os
import datetime

import pandas as pd
import numpy as np
import boto3
from dotenv import load_dotenv

from tools import mongoDB_tools as DB_tools
from main import run
import pymongo
import io

def connect_to_s3():
  s3 = boto3.client('s3',
    endpoint_url = os.environ['S3_ENDPOINT'],
    config = boto3.session.Config(signature_version = 's3v4'),
    aws_access_key_id = os.environ['S3_ID'],
    aws_secret_access_key = os.environ['S3_SECRET'],
    aws_session_token = None)
  return s3

def process_file(file_id):
  load_dotenv() # load environment variables from .env file

  myclient = pymongo.MongoClient(os.environ['DATABASE_URL'])
  db = myclient[os.environ['DATABASE_NAME']]

  #connexion à la collection files de mongoDB
  files = db.files

  #transformation du file_id de string a ObjectId
  file_id_object = DB_tools.object_file(file_id)

  #extraire la ligne de files qui correspondant au file_id
  information = DB_tools.find_file(files, file_id_object)

  if information is None:
    abort(404, description="Resource not found")

  #mise à jour du status du fichier à en cours
  resultat = DB_tools.update_status(files,file_id_object,"in_process")

  #insertion de lecture et traitement du dataset
  s3 = connect_to_s3()
  Key= "sensors/" + str(information["sensor_id"]) + "/" + file_id + ".csv"
  response = s3.get_object(Bucket=os.environ['S3_BUCKET'], Key = Key)
  content = response['Body'].read().decode('utf-8')
  data = pd.read_csv(io.StringIO(content), delimiter=";")
  dataset = run(data)

  #insertion des colonnes manquantes dans le dataset
  dataset["sensor_id"] = str(information["sensor_id"])
  dataset["file_id"] = str(file_id)
  dataset["created_at"] = datetime.datetime.now()
  dataset["updated_at"] = datetime.datetime.now()

  data_dict = dataset.to_dict("records")

  #connexion à la collection records de mongoDB
  records=db.records

  #Insertion des données dans la BDD mongoDB
  records.insert_many(data_dict)

  #mise à jour du status du fichier à terminé
  fin = DB_tools.update_status(files,file_id_object,"processed")

  #fermeture du lien avec la BDD
  myclient.close()

  return {"message": "success"}, 201