from flask import Flask, abort, jsonify, make_response, request
import os
import datetime

import json
from main import run

from process import process_file

DEFAULT_PORT = "8080"

app = Flask(__name__)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


HTTP_METHODS = ["GET", "POST"]

@app.route("/", methods=HTTP_METHODS)
def root():
    data = json.loads(request.get_data())
    result = process_file(data['file_id'])
    return result


if __name__ == "__main__":
  # Scaleway's system will inject a PORT environment variable on which your application should start the server.
  port_env =  os.getenv("PORT", DEFAULT_PORT)
  port = int(port_env)
  app.run(debug=True, host="0.0.0.0", port=port)
