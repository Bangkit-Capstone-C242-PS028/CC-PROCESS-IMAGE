from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten


def feature_extraction(image_array):
    base_model_vgg = ResNet50V2(
        weights="imagenet", include_top=False, input_shape=(450, 450, 3)
    )
    output = base_model_vgg.layers[-1].output
    output = Flatten()(output)
    model = Model(inputs=base_model_vgg.input, outputs=output)

    features = model.predict(image_array)
    return features
