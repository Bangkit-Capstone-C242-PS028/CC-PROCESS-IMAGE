from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten
from tensorflow.keras.applications.densenet import DenseNet121


def feature_extraction(image_array):
    base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    output = base_model.layers[-1].output
    output = Flatten()(output)
    model = Model(inputs=base_model.input, outputs=output)
    features = model.predict(image_array)
    return features
