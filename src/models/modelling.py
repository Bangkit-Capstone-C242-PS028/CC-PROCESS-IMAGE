import joblib


def modelling(features):
    model_path = "src/models/best_xgb_model_r50.pkl"
    loaded_model = joblib.load(model_path)

    predictions = loaded_model.predict(features)
    print("Predictions:", predictions)
    return predictions
