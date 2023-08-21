from flask import Flask, request, jsonify
from lightgbm import Booster
import shap
import numpy as np
import pandas as pd

app = Flask(__name__)

model = Booster(model_file='final_model.txt')

df = pd.read_csv('df_final_1000.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
for col in df.columns:
    try:
        df[col] = df[col].astype(float)
    except Exception as e:
        print(f"Error with column {col}: {e}")


model.params['objective'] = 'binary' # or whatever is appropriate

explainer = shap.TreeExplainer(model)


@app.route('/predict/<int:row_num>', methods=['GET'])
def predict(row_num):
    if row_num < 0 or row_num >= len(df):
        return jsonify({"error": "Invalid row number"}), 400

    sample = df.iloc[row_num, :]



    sample_df = sample.to_frame().T

    prediction = model.predict(sample_df)[0]
    shap_values = explainer.shap_values(sample_df)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    top_features_idx = np.argsort(np.abs(shap_values[0]))[-3:]
    top_features = sample_df.columns[top_features_idx].tolist()

    user_data = {}
    for col in top_features:
        user_data[col] = sample[col]
    return jsonify({
        "prediction": bool(prediction > 0.5),
        "top_features": top_features,
        "user_data": user_data
    })


@app.route('/get_data_for_features', methods=['GET'])
def get_data_for_features():
    feature_0 = request.args.get('feature_0')
    feature_1 = request.args.get('feature_1')
    feature_2 = request.args.get('feature_2')

    if not all([feature_0, feature_1, feature_2]):
        return jsonify({"error": "All three features must be provided!"}), 400

    try:
        raw_data = df[[feature_0, feature_1, feature_2]].to_dict(orient='list')
    except KeyError:
        return jsonify({"error": "One or more features are invalid!"}), 400
    return jsonify(raw_data)


if __name__ == '__main__':
    app.run(port=5003)
