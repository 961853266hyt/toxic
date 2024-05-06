import joblib
# 加载保存的向量化器
labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
vectorizer_path = './SVC/SVC_vectorizer.joblib'
scv_vectorizer = joblib.load(vectorizer_path)

def predict_labels(comment, vectorizer, loaded_models):
    # 使用提供的向量化器对评论进行向量化
    comment_vectorized = vectorizer.transform([comment])

    # 为每个标签进行预测
    predictions = {}
    for label, model in loaded_models.items():
        # 使用加载的模型进行预测
        prediction = model.predict(comment_vectorized)
        predictions[label] = prediction[0]

    return predictions

if __name__ == '__main__':
    # 加载保存的模型
    loaded_models = {}
    for label in labels:
        model_path = f'./SVC/linear_svc_model_{label}.joblib'
        loaded_models[label] = joblib.load(model_path)
    comment = "Fuck you!"
    # 对评论进行预测
    predictions = predict_labels(comment, scv_vectorizer, loaded_models)

    # 打印预测结果
    for label, prediction in predictions.items():
        print(f'Predicted label for {label}: {prediction}')