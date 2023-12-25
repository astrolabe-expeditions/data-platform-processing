from flask import Flask, abort, jsonify
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

DEFAULT_PORT = "8080"


app = Flask(__name__)

def connect_to_s3():
  s3 = boto3.client('s3',
                     endpoint_url = os.environ['SCW_ENDPOINT'],
                     config = boto3.session.Config(signature_version = 's3v4'),
                     aws_access_key_id = os.environ['SCW_ACCESS_KEY_ID'],
                     aws_secret_access_key = os.environ['SCW_SECRET_ACCESS_KEY'],
                     aws_session_token = None)
  return s3

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/process/<file_id>", methods=["POST"])
def root(file_id):
  load_dotenv() # load environment variables from .env file

  myclient = pymongo.MongoClient(os.environ['MONGO_URI'])
  db = myclient[os.environ['MONGO_DATABASE']]

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
  response = s3.get_object(Bucket=os.environ['SCW_BUCKET'], Key = Key)
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


if __name__ == "__main__":
  # Scaleway's system will inject a PORT environment variable on which your application should start the server.
  port_env =  os.getenv("PORT", DEFAULT_PORT)
  port = int(port_env)
  app.run(debug=True, host="0.0.0.0", port=port)
