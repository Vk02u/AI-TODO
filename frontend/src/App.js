import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTodos();
  }, []);

  function loadTodos() {
    fetch('http://localhost:8000/todos')
      .then(response => response.json())
      .then(data => {
        setTodos(data);
      })
      .catch(error => {
        console.log('Error loading todos:', error);
      });
  }

  function addTodo(e) {
    e.preventDefault();
    if (newTodo.trim() === '') return;

    fetch('http://localhost:8000/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: newTodo.trim() }),
    })
    .then(response => response.json())
    .then(todo => {
      setTodos([...todos, todo]);
      setNewTodo('');
    })
    .catch(error => {
      console.log('Error adding todo:', error);
    });
  }

  function generateTodos(e) {
    e.preventDefault();
    if (goal.trim() === '') return;

    setLoading(true);
    fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal: goal.trim() }),
    })
    .then(response => response.json())
    .then(generatedTodos => {
      setTodos([...todos, ...generatedTodos]);
      setGoal('');
      setLoading(false);
    })
    .catch(error => {
      console.log('Error generating todos:', error);
      setLoading(false);
    });
  }

  function deleteTodo(todoId) {
    fetch(`http://localhost:8000/todos/${todoId}`, {
      method: 'DELETE',
    })
    .then(() => {
      const updatedTodos = todos.filter(todo => todo.id !== todoId);
      setTodos(updatedTodos);
    })
    .catch(error => {
      console.log('Error deleting todo:', error);
    });
  }

  function clearAllTodos() {
    if (window.confirm('Clear all todos?')) {
      fetch('http://localhost:8000/todos', {
        method: 'DELETE',
      })
      .then(() => {
        setTodos([]);
      })
      .catch(error => {
        console.log('Error clearing todos:', error);
      });
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>My Todo App</h1>
          <p>Simple todo list with AI help</p>
        </header>

        <div className="main-content">
          <section className="ai-section">
            <h2>Get AI Help</h2>
            <form onSubmit={generateTodos} className="goal-form">
              <input
                type="text"
                placeholder="What do you want to do? (e.g., plan a trip)"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                className="goal-input"
                disabled={loading}
              />
              <button type="submit" className="generate-btn" disabled={loading}>
                {loading ? 'Thinking...' : 'Get Ideas'}
              </button>
            </form>
          </section>

          <section className="manual-section">
            <h2>Add Your Own</h2>
            <form onSubmit={addTodo} className="todo-form">
              <input
                type="text"
                placeholder="Add a task"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                className="todo-input"
              />
              <button type="submit" className="add-btn">Add</button>
            </form>
          </section>

          {todos.length > 0 && (
            <section className="controls">
              <button onClick={clearAllTodos} className="clear-btn">
                Clear All
              </button>
            </section>
          )}

          <section className="todo-list">
            {todos.length === 0 ? (
              <div className="empty-state">
                <p>No tasks yet. Add some or get AI ideas!</p>
              </div>
            ) : (
              <ul className="todos">
                {todos.map((todo) => (
                  <li key={todo.id} className="todo-item">
                    <div className="todo-content">
                      <span className="todo-text">{todo.text}</span>
                      {todo.is_generated && (
                        <span className="ai-badge" title={`From: ${todo.original_goal}`}>
                          AI
                        </span>
                      )}
                    </div>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="delete-btn"
                      title="Delete"
                    >
                      ×
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;
