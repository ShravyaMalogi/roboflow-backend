from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_URL = "https://serverless.roboflow.com/room-surface-segmentation/1"

@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "api_key": ROBOFLOW_API_KEY,
        "inputs": {
            "image": {
                "type": "base64",
                "value": encoded_image
            }
        }
    }

    response = requests.post(ROBOFLOW_URL, json=payload)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
