
import React, { useState } from 'react';
import { getInsights } from '../api';

const AgentInsights = () => {
    const [question, setQuestion] = useState('');
    const [insights, setInsights] = useState('');
    const [loading, setLoading] = useState(false);

    const handleGetInsights = () => {
        setLoading(true);
        getInsights(question)
            .then(res => {
                setInsights(res.data.insights);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    };

    return (
        <div>
            <h2>Agent Insights</h2>
            <textarea 
                value={question} 
                onChange={(e) => setQuestion(e.target.value)} 
                placeholder="Ask a question about the vehicle..."
            />
            <button onClick={handleGetInsights} disabled={loading}>
                {loading ? 'Getting Insights...' : 'Get AI Feedback'}
            </button>
            {insights && <pre>{insights}</pre>}
        </div>
    );
};

export default AgentInsights;
