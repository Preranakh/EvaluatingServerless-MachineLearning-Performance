import os
import PIL.Image as Image

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


class Predictor:
    def __init__(self):
        self.classifier_model = (
            "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
        )
        self.IMAGE_SHAPE = (224, 224)
        self._load_model()
        self._load_labels()

    def _load_model(self):
        self.classifier = tf.keras.Sequential(
            [hub.KerasLayer(self.classifier_model, input_shape=self.IMAGE_SHAPE + (3,))]
        )

    def _load_labels(self):
        _labels_path = tf.keras.utils.get_file(
            "ImageNetLabels.txt",
            "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt",
        )
        self.imagenet_labels = np.array(open(_labels_path).read().splitlines())

    def predict(self, img_path) -> str:
        if not os.path.isfile(img_path):
            raise Exception("File Not Found")
        im = Image.open(img_path).resize(self.IMAGE_SHAPE)
        im = np.array(im) / 255.0
        im_expanded_dim = im[np.newaxis, ...]

        result = self.classifier.predict(im_expanded_dim)
        predicted_class = tf.math.argmax(result[0], axis=-1)
        return self.imagenet_labels[predicted_class]

    def __call__(self, img_path):
        self.predict(img_path)
