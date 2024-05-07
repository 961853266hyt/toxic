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
        {Object.entries(predictions).map(([modelName, modelResult]) => (
          <li key={modelName}>
            <h3>{modelName}</h3>
            <ul>
              {modelResult.map((result, index) => (  
                <li key={index}>
                  <div className={styles.modelResult}>
                    {Object.entries(result).map(([label, value]) => (
                      <span key={label}>
                        {value.toString()} &nbsp;&nbsp;
                      </span>
                    ))}
                  </div>
                </li>
              ))}
            </ul>
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
