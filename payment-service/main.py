from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Payment Service", version="1.0.0")

# In-memory database
payments_db = {}
payment_counter = 1


class Payment(BaseModel):
    order_id: int
    user_id: int
    amount: float
    method: str


class PaymentResponse(Payment):
    id: int
    status: str
    created_at: str


@app.get("/")
async def root():
    return {"service": "payment-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/payments", response_model=PaymentResponse)
async def create_payment(payment: Payment):
    global payment_counter
    try:
        payment_id = payment_counter
        payment_counter += 1
        
        payments_db[payment_id] = {
            "id": payment_id,
            "order_id": payment.order_id,
            "user_id": payment.user_id,
            "amount": payment.amount,
            "method": payment.method,
            "status": "PENDING",
            "created_at": datetime.now().isoformat()
        }
        return payments_db[payment_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/payments", response_model=List[PaymentResponse])
async def list_payments(skip: int = 0, limit: int = 10):
    try:
        payments = list(payments_db.values())
        return payments[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int):
    try:
        if payment_id not in payments_db:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payments_db[payment_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/payments/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: int, payment: Payment):
    try:
        if payment_id not in payments_db:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        payments_db[payment_id].update({
            "order_id": payment.order_id,
            "user_id": payment.user_id,
            "amount": payment.amount,
            "method": payment.method
        })
        return payments_db[payment_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/payments/{payment_id}")
async def delete_payment(payment_id: int):
    try:
        if payment_id not in payments_db:
            raise HTTPException(status_code=404, detail="Payment not found")
        del payments_db[payment_id]
        return {"message": "Payment deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
