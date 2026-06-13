from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Order Service", version="1.0.0")

# In-memory database
orders_db = {}
order_counter = 1


class Order(BaseModel):
    user_id: int
    product: str
    quantity: int
    price: float


class OrderResponse(Order):
    id: int
    status: str
    created_at: str


@app.get("/")
async def root():
    return {"service": "order-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/orders", response_model=OrderResponse)
async def create_order(order: Order):
    global order_counter
    try:
        order_id = order_counter
        order_counter += 1
        
        orders_db[order_id] = {
            "id": order_id,
            "user_id": order.user_id,
            "product": order.product,
            "quantity": order.quantity,
            "price": order.price,
            "status": "PENDING",
            "created_at": datetime.now().isoformat()
        }
        return orders_db[order_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders", response_model=List[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 10):
    try:
        orders = list(orders_db.values())
        return orders[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    try:
        if order_id not in orders_db:
            raise HTTPException(status_code=404, detail="Order not found")
        return orders_db[order_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: Order):
    try:
        if order_id not in orders_db:
            raise HTTPException(status_code=404, detail="Order not found")
        
        orders_db[order_id].update({
            "user_id": order.user_id,
            "product": order.product,
            "quantity": order.quantity,
            "price": order.price
        })
        return orders_db[order_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    try:
        if order_id not in orders_db:
            raise HTTPException(status_code=404, detail="Order not found")
        del orders_db[order_id]
        return {"message": "Order deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
