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

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


HTTP_METHODS = ["GET", "POST"]

@app.route("/", methods=HTTP_METHODS)
def root():
    print(request.get_data(), flush=True)
    response = make_response("Hello from container")
    return response


@app.route("/process/<file_id>", methods=["POST"])
def root(file_id):
  result = process_file(content['file_id'])
  return result


if __name__ == "__main__":
  # Scaleway's system will inject a PORT environment variable on which your application should start the server.
  port_env =  os.getenv("PORT", DEFAULT_PORT)
  port = int(port_env)
  app.run(debug=True, host="0.0.0.0", port=port)
