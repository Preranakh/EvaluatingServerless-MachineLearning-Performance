import os
import uuid
from traceback import print_exc

from loguru import logger
from flask import Flask, jsonify, request

from classifier import Predictor
from classifier.util import download_img_from_url

model = Predictor()

app = Flask(__name__)
if not os.path.isdir("tmp/"):
    os.mkdir("tmp/")


@app.route("/", methods=["GET"])
def root_check():
    logger.info("Health check!!")
    return "Welcome to MobileNet Flask App! OS Project 2022."


@app.route("/predict", methods=["POST"])
def predict():
    logger.info("Predict endpoint")
    URL_DOWNLOAD_SUCCESS = False
    content_type = request.headers.get("Content-Type")
    if content_type.startswith("multipart/form-data") or content_type.startswith(
        "application/x-www-form-urlencoded"
    ):
        x_api_key = request.headers.get("x-api-key")
        if not x_api_key == "1234":
            return jsonify({"message": "Incorrect credentials"}), 401
        files = request.files
        if not files:
            file_path = download_img_from_url(request.form.get("image"))
            if file_path == "DOWNLOAD_ERROR":
                return jsonify({"message": "Missing Image in the request"}), 400
            URL_DOWNLOAD_SUCCESS = True
        elif not files.get("image"):
            return jsonify({"message": "Missing image parameter in the request"}), 400

        if not URL_DOWNLOAD_SUCCESS:
            im = files.get("image")
            ext = im.filename.split(".")[-1]
            if ext.lower() not in ["jpg", "png", "jpeg"]:
                return jsonify({"message": "Unsupported image format"}), 400
            filename = uuid.uuid4().hex
            file_path = os.path.join(
                os.path.dirname(__file__), "tmp", filename + "." + ext
            )
            im.save(file_path)
        try:
            prediction = model.predict(file_path)
        except:
            logger.error("Server error!")
            logger.error(print_exc())
            return {"message": "Server error!"}, 500
        return jsonify({"message": "Success", "Prediction": prediction}), 200
    else:
        return jsonify({"message": "Content-Type not supported!"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0")

# gunicorn --workers 1 --bind 0.0.0.0:5000 app:app
