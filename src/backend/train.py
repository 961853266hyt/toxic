# /src/backend/train.py
from flask import Flask, jsonify, request
import joblib
from flask_cors import CORS
from tokenizers import identity_tokenizer
from SVC import SVC_predict
from Seq import Seq_predict

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

def combine(pred1, pred2, pred3):
    result = {}
    result['Logistic Regression'] = pred1
    result['Support Vector Classifier'] = pred2
    result['Sequential Neural Network'] = pred3
    print("bkkkkk:", result)
    return result

@app.route('/api/predict', methods=['POST'])
def handle_predict():
    data = request.json
    comment = data.get('comment', '')

    if not comment:
        return jsonify({'error': 'No comment provided'}), 400

    predictions = predict([comment])  # logistic regression
    pre_SVC = SVC_predict(comment) 
    pre_Seq = Seq_predict(comment)
    final_pred = combine(to_json(predictions), pre_SVC, pre_Seq)
    return jsonify(final_pred), 200

if __name__ == '__main__':
    app.run(debug=True)
