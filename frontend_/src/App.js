import React, { useState } from 'react';

function App() {
  const [goal, setGoal] = useState('');
  const [checklist, setChecklist] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal }),
    });
    const data = await response.json();
    setChecklist(data.checklist);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Task Assistant</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your goal"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
        />
        <button type="submit">Generate Checklist</button>
      </form>

      <ul>
        {checklist.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
