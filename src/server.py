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
  result = process_file(content['file_id'])
  return result


if __name__ == "__main__":
  # Scaleway's system will inject a PORT environment variable on which your application should start the server.
  port_env =  os.getenv("PORT", DEFAULT_PORT)
  port = int(port_env)
  app.run(debug=True, host="0.0.0.0", port=port)
