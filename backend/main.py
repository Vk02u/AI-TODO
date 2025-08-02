from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
import json
from datetime import datetime

# API key
GOOGLE_API_KEY = "AIzaSyBM68gk1KUgnq2eoZFEfc5YKg-bBRzrKLw"

genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoItem(BaseModel):
    id: Optional[str] = None
    text: str
    created_at: Optional[str] = None
    is_generated: bool = False
    original_goal: Optional[str] = None

class GoalInput(BaseModel):
    goal: str

# data storage
todos = []
todo_counter = 0

def save_todos():
    with open("todos.json", "w") as f:
        data = []
        for todo in todos:
            data.append(todo.dict())
        json.dump(data, f)

def load_todos():
    global todos, todo_counter
    try:
        with open("todos.json", "r") as f:
            data = json.load(f)
            todos = []
            for item in data:
                todo = TodoItem(**item)
                todos.append(todo)
            
            if len(todos) > 0:
                max_id = 0
                for todo in todos:
                    if todo.id and todo.id.isdigit():
                        if int(todo.id) > max_id:
                            max_id = int(todo.id)
                todo_counter = max_id + 1
            else:
                todo_counter = 0
    except FileNotFoundError:
        todos = []
        todo_counter = 0
    except:
        todos = []
        todo_counter = 0

def generate_todos(goal):
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
Create a list of 3-5 simple and actionable todos for the goal: "{goal}"

Examples of good todos:
- Pack your bags
- Book accommodation  
- Research local attractions
- Check travel documents
- Make a packing list

Return only the list of todos, one per line, without numbers or bullet points. Keep them simple and actionable.
"""
    response = model.generate_content(prompt)
    text = response.text
    
    lines = text.strip().splitlines()
    checklist = []
    for line in lines:
        line = line.strip()
        if line.startswith('-'):
            line = line[1:].strip()
        if line.startswith('•'):
            line = line[1:].strip()
        if line:
            checklist.append(line)
    
    return checklist[:5]

@app.on_event("startup")
async def startup_event():
    load_todos()

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    return todos

@app.post("/todos", response_model=TodoItem)
async def add_todo(todo: TodoItem):
    global todo_counter
    todo.id = str(todo_counter)
    todo_counter = todo_counter + 1
    todo.created_at = datetime.now().isoformat()
    todos.append(todo)
    save_todos()
    return todo

@app.post("/generate", response_model=List[TodoItem])
async def generate_checklist(data: GoalInput):
    global todo_counter
    try:
        checklist_items = generate_todos(data.goal)
        generated_todos = []
        
        for item in checklist_items:
            todo = TodoItem(
                text=item,
                is_generated=True,
                original_goal=data.goal
            )
            todo.id = str(todo_counter)
            todo_counter = todo_counter + 1
            todo.created_at = datetime.now().isoformat()
            generated_todos.append(todo)
            todos.append(todo)
        
        save_todos()
        return generated_todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: str, updated_todo: TodoItem):
    for i in range(len(todos)):
        if todos[i].id == todo_id:
            updated_todo.id = todo_id
            updated_todo.created_at = todos[i].created_at
            todos[i] = updated_todo
            save_todos()
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    global todos
    original_count = len(todos)
    
    new_todos = []
    for todo in todos:
        if str(todo.id) != str(todo_id):
            new_todos.append(todo)
    
    todos = new_todos
    
    if len(todos) == original_count:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    
    save_todos()
    return {"message": f"Todo {todo_id} deleted"}

@app.delete("/todos")
async def clear_all_todos():
    global todos
    todos = []
    save_todos()
    return {"message": "All todos cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
