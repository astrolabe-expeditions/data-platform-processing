from flask import Flask
import os

from tools import mongoDB_tools as DB_tools
from main import run
import pymongo

DEFAULT_PORT = "8080"


app = Flask(__name__)

@app.route("/process/<file_id>", methods=["POST"])
def root(file_id):
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
  dataset = run()

  #insertion des colonnes manquantes dans le dataset
  dataset["sensor_id"]=information["sensor_id"]
  dataset["id"] = [file_id for i in range(len(dataset))]
    
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