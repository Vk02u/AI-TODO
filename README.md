# My Todo App

A simple todo app that uses AI to help you make task lists.

## What it does

- Add your own tasks
- Get AI suggestions for tasks
- Delete tasks
- Clear all tasks
- Save tasks to your computer

## Setup

### What you need
- Node.js (version 14 or higher)
- Python (version 3.8 or higher)
- Google Gemini API key

### Install

1. **Backend setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Frontend setup**
   ```bash
   cd frontend
   npm install
   ```

3. **Add API key**
   - Open `backend/main.py`
   - Find the line with `GOOGLE_API_KEY`
   - Replace it with your own key

### Run the app

1. **Start backend**
   ```bash
   cd backend
   python main.py
   ```

2. **Start frontend**
   ```bash
   cd frontend
   npm start
   ```

## How to use

### Add tasks manually
1. Type your task in the "Add Your Own" box
2. Click "Add" button

### Get AI help
1. Type what you want to do in "Get AI Help" box
2. Click "Get Ideas" button
3. AI will give you 3-5 task suggestions

### Delete tasks
- Click the "×" button next to any task to delete it
- Click "Clear All" to delete all tasks

## API

- `GET /todos` - Get all todos
- `POST /todos` - Add a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo
- `DELETE /todos` - Delete all todos
- `POST /generate` - Get AI suggestions

## Files

```
AI-TODO/
├── frontend/          # React app
│   ├── src/
│   │   ├── App.js    # Main app
│   │   ├── App.css   # Styles
│   │   └── index.js  # Start file
│   └── package.json
├── backend/           # Python server
│   ├── main.py       # Server code
│   ├── requirements.txt
│   └── todos.json    # Data file
└── README.md
```

## Notes

- Tasks are saved in `backend/todos.json`
- AI gives you 3-5 simple tasks
- Works on phone and computer

## Problems

**Backend won't start**
- Make sure you ran `pip install -r requirements.txt`
- Check if port 8000 is free

**Frontend won't connect**
- Make sure backend is running
- Check browser console for errors

**AI not working**
- Check your API key is right
- Make sure you have internet
- Check you have API credits

## License

MIT License 