from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Notification Service", version="1.0.0")

# In-memory database
notifications_db = {}
notification_counter = 1


class Notification(BaseModel):
    user_id: int
    message: str
    type: str


class NotificationResponse(Notification):
    id: int
    status: str
    created_at: str


@app.get("/")
async def root():
    return {"service": "notification-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/notifications", response_model=NotificationResponse)
async def create_notification(notification: Notification):
    global notification_counter
    try:
        notification_id = notification_counter
        notification_counter += 1
        
        notifications_db[notification_id] = {
            "id": notification_id,
            "user_id": notification.user_id,
            "message": notification.message,
            "type": notification.type,
            "status": "PENDING",
            "created_at": datetime.now().isoformat()
        }
        return notifications_db[notification_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications", response_model=List[NotificationResponse])
async def list_notifications(skip: int = 0, limit: int = 10):
    try:
        notifications = list(notifications_db.values())
        return notifications[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: int):
    try:
        if notification_id not in notifications_db:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notifications_db[notification_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification(notification_id: int, notification: Notification):
    try:
        if notification_id not in notifications_db:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notifications_db[notification_id].update({
            "user_id": notification.user_id,
            "message": notification.message,
            "type": notification.type
        })
        return notifications_db[notification_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: int):
    try:
        if notification_id not in notifications_db:
            raise HTTPException(status_code=404, detail="Notification not found")
        del notifications_db[notification_id]
        return {"message": "Notification deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
