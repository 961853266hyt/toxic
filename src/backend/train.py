# import joblib
# labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
# test_comments = ["You are a stupid fool!"]

# def identity_tokenizer(text):
#     return text

# def load_and_predict(test_comments):
#     # 加载向量器
#     vectorizer = joblib.load('logistic_vectorizer.joblib')
#     # 将评论转换为特征向量
#     test_features = vectorizer.transform(test_comments)

#     # 加载模型并进行预测
#     predictions = {}
#     for label in labels:
#         model = joblib.load(f'logistic_model_{label}.joblib')
#         # 获取正类概率
#         proba_predictions = model.predict_proba(test_features)[:, 1]
#         predictions[label] = proba_predictions

#     return predictions

# #       { label: 'toxic', value: 0.9028 },
# #       { label: 'severe_toxic', value: 0.0830 },
# #       { label: 'obscene', value: 0.6680 },
# #       { label: 'threat', value: 0.0351 },
# #       { label: 'insult', value: 0.5695 },
# #       { label: 'identity_hate', value: 0.0877 }
# def ToJson(results): # {label:[labelname], value:[value]}
#     json = []
#     for label in labels:
#         json.append({"label": label, "value": results[label][0]})
#     return json


# if __name__ == '__main__':
#     results = load_and_predict(test_comments)
#     print(results)
#     for label in labels:
#         print(f"Predictions for '{label}': {results[label]}")

#     print("Json:")
#     print(ToJson(results))

# /src/backend/train.py
from flask import Flask, jsonify, request
import joblib
from flask_cors import CORS
from tokenizers import identity_tokenizer

app = Flask(__name__)
CORS(app)

# 加载模型
labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
vectorizer = joblib.load('logistic_vectorizer.joblib')
models = {label: joblib.load(f'logistic_model_{label}.joblib') for label in labels}

def predict(test_comments):
    # 加载向量器
    vectorizer = joblib.load('logistic_vectorizer.joblib')
    # 将评论转换为特征向量
    test_features = vectorizer.transform(test_comments)

    # 加载模型并进行预测
    predictions = {}
    for label in labels:
        model = joblib.load(f'logistic_model_{label}.joblib')
        # 获取正类概率
        proba_predictions = model.predict_proba(test_features)[:, 1]
        # four decimal places
        proba_predictions = [round(x, 4) for x in proba_predictions]
        predictions[label] = proba_predictions

    return predictions

def to_json(results): 
    json_data = []
    for label in labels:
        json_data.append({"label": label, "value": results[label][0]})
    return json_data

@app.route('/api/predict', methods=['POST'])
def handle_predict():
    data = request.json
    comment = data.get('comment', '')

    if not comment:
        return jsonify({'error': 'No comment provided'}), 400

    predictions = predict([comment])  # 将评论转换为列表
    return jsonify(to_json(predictions)), 200

if __name__ == '__main__':
    app.run(debug=True)
