import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input


def preprocess(image_path):
    image = load_img(image_path, target_size=(450, 450))  # Resize to match VGG16 input
    image_array = img_to_array(image)  # Convert to numpy array
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = preprocess_input(image_array)  # Preprocess as per VGG16 requirements
    return image_array, image
