import tensorflow as tf
import numpy as np


def modelling(features):
    interpreter = tf.lite.Interpreter(model_path="src/models/final_model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_shape = input_details[0]["shape"]
    if np.array_equal(input_shape, [1, 224, 224, 3]):  # Compare arrays element-wise
        # Reshape features to original image dimensions and add batch dimension
        features = features.reshape(1, 224, 224, 1)  # Reshape to (1, 224, 224, 1)
        features = np.repeat(features, 3, axis=-1)  # Repeat to (1, 224, 224, 3)
    else:
        features = features.reshape(input_shape)  # Reshape to the expected shape

    interpreter.set_tensor(input_details[0]["index"], features.astype(np.float32))
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]["index"])

    return [np.argmax(predictions), np.max(predictions)]
