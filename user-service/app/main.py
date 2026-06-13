from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="User Service", version="1.0.0")

# In-memory database (simple, no PostgreSQL needed for testing)
users_db = {}
user_counter = 1


class User(BaseModel):
    name: str
    email: str
    phone: str


class UserResponse(User):
    id: int
    created_at: str


@app.get("/")
async def root():
    return {"service": "user-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/users", response_model=UserResponse)
async def create_user(user: User):
    global user_counter
    try:
        user_id = user_counter
        user_counter += 1
        
        users_db[user_id] = {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "created_at": datetime.now().isoformat()
        }
        return users_db[user_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 10):
    try:
        users = list(users_db.values())
        return users[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    try:
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        return users_db[user_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    try:
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        users_db[user_id].update({
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        })
        return users_db[user_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    try:
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        del users_db[user_id]
        return {"message": "User deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
