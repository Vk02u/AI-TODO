# AI Todo App

A basic todo app with AI task suggestions.

## Features

* Add tasks
* Get AI task ideas
* Delete or clear tasks

## Setup

### Requirements

* Node.js
* Python (FastAPI)
* Google Gemini API key

### Add API Key

Edit `backend/main.py` and paste your Gemini API key in `GOOGLE_API_KEY = ""`.

## Run the App

```bash
# Start backend
cd backend
pip install -r requirements.txt
python main.py

# Start frontend
cd frontend
npm install
npm start
```

## Usage

* **Add task:** Type and click "Add"
* **AI ideas:** Type and click "Get Ideas"
* **Delete task:** Click `×`
* **Clear all:** Click "Clear All"

---
