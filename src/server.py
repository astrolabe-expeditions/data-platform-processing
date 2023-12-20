from flask import Flask
import os

import pandas as pd
import numpy as np
import boto3
from dotenv import load_dotenv

from tools import mongoDB_tools as DB_tools
from main import run
import pymongo

DEFAULT_PORT = "8080"


app = Flask(__name__)

def s3_create():
  s3 = boto3.resource('s3',
                     endpoint_url = os.environ['SCW_ENDPOINT'],
                     config = boto3.session.Config(signature_version = 's3v4'),
                     aws_access_key_id = os.environ['SCW_ACCESS_KEY_ID'],
                     aws_secret_access_key = os.environ['SCW_SECRET_ACCESS_KEY'],
                     aws_session_token = None)
  return s3

@app.route("/process/<file_id>", methods=["POST"])
def root(file_id):
  load_dotenv() # load environment variables from .env file

  myclient = pymongo.MongoClient('mongodb+srv://daullethomas631:Thomas2002@cluster0.chgct4d.mongodb.net/?retryWrites=true&w=majority')
  db = myclient["Astrolabe"]

  #connexion à la collection files de mongoDB
  files = db.files

  #transformation du file_id de string a ObjectId
  file_id_object = DB_tools.object_file(file_id)

  #extraire la ligne de files qui correspondant au file_id
  information = DB_tools.find_file(files, file_id_object)
  print(information)

  #mise à jour du status du fichier à en cours
  resultat = DB_tools.update_status(files,file_id_object,"in_process")
  print(resultat.modified_count)

  #insertion de lecture et traitement du dataset
  s3 = s3_create()
  Key= "sensor/" + information["sensor_id"]+"/"+file_id+".csv"
  files = s3.Bucket('astrolabe-expeditions-data').Object(key=Key)
  response=files.get()
  dataset = run(response['Body'].read())

  #insertion des colonnes manquantes dans le dataset
  dataset["sensor_id"]=information["sensor_id"]
  dataset["id"] = file_id
    
  #connexion à la collection records de mongoDB
  records=db.records
    
  #Insertion des données dans la BDD mongoDB
  records.insert_many(dataset)

  #mise à jour du status du fichier à terminé
  fin = DB_tools.update_status(files,file_id_object,"processed")
  print(fin.modified_count)

  #fermeture du lien avec la BDD
  myclient.close()
  


if __name__ == "__main__":
  # Scaleway's system will inject a PORT environment variable on which your application should start the server.
  port_env =  os.getenv("PORT", DEFAULT_PORT)
  port = int(port_env)
  app.run(debug=True, host="0.0.0.0", port=port)