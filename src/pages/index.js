import React, { useState } from 'react';
import styles from '../styles/Home.module.css'; // 导入样式文件

const Predictions = () => {
  const [comment, setComment] = useState('');
  const [predictions, setPredictions] = useState(null);

  const handleInputChange = (event) => {
    setComment(event.target.value);
  };

  const handlePredict = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comment }), // 将评论作为JSON字符串发送
      });
      const data = await response.json(); // 解析后端返回的JSON数据
      console.log('Predictions:', data);

      // 设置预测结果状态
      setPredictions(data);
    } catch (error) {
      console.error('Error predicting labels:', error);
    }
  };

  // return a bar chart besides the text area, each bar represents a label and its height represents the value of the label in the predictions
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Comment Analyzer</h1>
      <div className={styles.inputContainer}>
        <textarea
          className={styles.textArea}
          value={comment}
          onChange={handleInputChange}
          placeholder="Enter your comment..."
        />
      </div>
      <button className={styles.button} onClick={handlePredict}>Show</button>
      <div> 
        {predictions && (
          <div className={styles.predictions}>
            <h2>Predictions:</h2>
            <ul>
              {predictions.map(prediction => (
                <li key={prediction.label}>
                  <strong>{prediction.label}:</strong> {prediction.value}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Predictions;
