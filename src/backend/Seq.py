from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
# 加载模型和tokenizer
model = load_model('./Seq/Seq_model.h5')
tokenizer = joblib.load('./Seq/Seq_tokenizer.joblib')

def predict_comments(model, tokenizer, comments, max_len):
    # 将文本转换为序列
    sequences = tokenizer.texts_to_sequences(comments)
    
    # 使用与训练相同的长度填充序列
    padded_sequences = pad_sequences(sequences, maxlen=max_len)
    
    # 使用模型进行预测
    predictions = model.predict(padded_sequences)
    
    # 创建一个空列表来存储结果
    results = []
    
    # 存储每个评论的预测结果
    for i, comment in enumerate(comments):
        comment_result = {"comment": comment, "labels": {}}
        for label_index, label in enumerate(labels):
            comment_result["labels"][label] = f"{predictions[i][label_index]:.4f}"
        results.append(comment_result)
    
    return results

def Seq_predict(comment):
    results = predict_comments(model, tokenizer, [comment], 100)
    temp = results[0]['labels']
    json_data = []
    for label in labels:
        json_data.append({"label": label, "value": temp[label]})
    return json_data

if __name__ == '__main__':
    # test_comments = ["Your post is a shit"]
    # # 调用修改后的测试函数
    # results = predict_comments(model, tokenizer, test_comments, 100)

    # # 在外部打印结果
    # for result in results:
    #     print(f"\nComment: '{result['comment']}'")
    #     print("Predicted labels:")
    #     for label, probability in result['labels'].items():
    #         print(f"  - {label} (Probability: {probability})")
    result = Seq_predict("fuck fuck fuck")
    print(result)