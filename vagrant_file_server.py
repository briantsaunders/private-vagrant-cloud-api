#!/usr/bin/python3

# import std libs
import glob
import json
import pathlib

# import third party libs
from flask import Flask, jsonify, send_file
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    local_path = pathlib.Path(f"/var/{path}")
    if ".box" in path:
        if local_path.exists():
            if local_path.is_file():
                response = send_file(local_path)
                response.headers.add("Content-Disposition", "attachment")
                return response
            else:
                response = jsonify({"error": f"{path} is not a file"})
                response.status_code = 400
                return response
    if local_path.exists():
        if local_path.is_dir():
            results = []
            search = pathlib.Path(local_path).glob("*.json")
            for result in search:
                results.append(result)
            if results:
                # should only be one .json in dir
                with open(results[0]) as json_file:
                    response = json.load(json_file)
                    return jsonify(response)
            else:
                response = jsonify({"error": f"{path} does not contain .json file"})
                response.status_code = 400
                return response
        else:
            response = jsonify({"error": f"local path {local_path} not a directory"})
            response.status_code = 400
            return response
    response = jsonify({"error": f"local path {local_path} does not exist"})
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)