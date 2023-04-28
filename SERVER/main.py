import base64
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from keras.models import Sequential, load_model
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

IMG_BREDTH = 30
IMG_HEIGHT = 60

# Define the Flask app
app = Flask(__name__)
CORS(app)

# Load the machine learning model
model = ...

def use_model(pic):
    pic= cv2.resize(pic, dsize=(IMG_BREDTH, IMG_HEIGHT), interpolation=cv2.INTER_CUBIC)
    model = load_model('best_waste_classifier.h5')
    if np.argmax(model.predict(np.expand_dims(pic, axis=0)), axis=1) == 0:
        classes = 'ORGANIC'
    elif np.argmax(model.predict(np.expand_dims(pic, axis=0)), axis=1) == 1:
        classes = 'RECYCLABLE'

    return classes


# Define the endpoint for receiving images
@app.route('/process_image', methods=['POST'])
def process_image():
    # Get the image data from the request
    image_data = request.json['image']

    # Decode the base64-encoded image data and convert it to a NumPy array
    image_data = base64.b64decode(image_data)
    image = np.array(Image.open(BytesIO(image_data)))

    # Process the image using the machine learning model
    result = use_model(image)

    # Return the result as a JSON object
    return jsonify({'result': result})


# Start the Flask app
if __name__ == '__main__':
    app.run(host='localhost', port=4544)
