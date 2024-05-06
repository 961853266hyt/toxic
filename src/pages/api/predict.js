// pages/api/predict.js

export default async function handler(req, res) {
    if (req.method === 'POST') {
        try {
            // 假设这里是向后端发送评论并获取预测结果的代码
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: req.body.comment }),
            });
            const data = await response.json();
            res.status(200).json(data);
        } catch (error) {
            console.error('Error predicting labels:', error);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    } else {
        res.status(405).json({ message: 'Method Not Allowed' });
    }
}
