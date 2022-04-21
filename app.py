import os
import uuid
from traceback import print_exc

from loguru import logger
from flask import Flask, jsonify, request

from classifier import Predictor

model = Predictor()

app = Flask(__name__)
if not os.path.isdir("tmp/"):
    os.mkdir("tmp/")


@app.route("/healthz", methods=["GET"])
def health_check():
    logger.info("here!!")
    return "Welcome to MobileNet Flask App!"


@app.route("/predict", methods=["POST"])
def predict():
    content_type = request.headers.get("Content-Type")
    if content_type.startswith("multipart/form-data"):
        x_api_key = request.headers.get("x-api-key")
        if not x_api_key == "1234":
            return jsonify({"message": "Incorrect credentials"}), 401
        files = request.files
        if not files:
            return jsonify({"message": "Missing Image in the request"}), 400
        elif not files.get("image"):
            return jsonify({"message": "Missing Image in the request"}), 400

        im = files.get("image")
        ext = im.filename.split(".")[-1]
        if ext.lower() not in ["jpg", "png", "jpeg"]:
            return jsonify({"message": "Unsupported image format"}), 400
        filename = uuid.uuid4().hex
        file_path = os.path.join(os.path.dirname(__file__), "tmp", filename + "." + ext)
        im.save(file_path)
        try:
            prediction = model.predict(file_path)
        except:
            logger.error("Server error!")
            logger.error(print_exc())
            return {"message": "Server error!"}, 500
        return jsonify({"message": "Success", "Prediction": prediction}), 200
    else:
        return "Content-Type not supported!"


if __name__ == "__main__":
    app.run()

# gunicorn --workers 1 --bind 0.0.0.0:5000 app:app
