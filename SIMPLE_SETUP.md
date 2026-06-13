# 🚀 SIMPLIFIED MICROSERVICES SETUP

## 📁 Simple Folder Structure

```
microservices/
├── user-service/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── order-service/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── payment-service/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── notification-service/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── k8s-deployments.yaml
```

---

## ⚡ FASTEST SETUP (3 STEPS)

### Step 1: Create Folders & Copy Files

```bash
# Create structure
mkdir -p microservices/{user-service,order-service,payment-service,notification-service}/{app}
cd microservices

# Copy for EACH service (same requirements.txt & Dockerfile)
for service in user-service order-service payment-service notification-service; do
  cp app__init__.py $service/app/__init__.py
  cp ${service}-main.py $service/app/main.py
  cp requirements-shared.txt $service/requirements.txt
  cp Dockerfile-shared $service/Dockerfile
done

# Copy docker-compose & k8s
cp docker-compose-all.yml docker-compose.yml
cp k8s-deployments.yaml k8s-deployments.yaml
```

### Step 2: Start All Services with Docker Compose

```bash
# One command to run ALL 4 services
docker-compose up -d

# Check status
docker-compose ps
```

### Step 3: Test Services

```bash
# User Service (8001)
curl http://localhost:8001/health

# Order Service (8002)
curl http://localhost:8002/health

# Payment Service (8003)
curl http://localhost:8003/health

# Notification Service (8004)
curl http://localhost:8004/health
```

---

## 📝 What's the Same?

| File | Status |
|------|--------|
| `requirements.txt` | ✅ ONE for all 4 services |
| `Dockerfile` | ✅ ONE for all 4 services |
| `docker-compose.yml` | ✅ Runs all 4 at once |

---

## 📊 What's Different?

Each service has:
- ✅ Own `main.py` (different business logic)
- ✅ Own port (8001, 8002, 8003, 8004)
- ✅ Own container name
- ✅ Own health check

---

## 🐳 Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View logs of specific service
docker-compose logs -f user-service

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild images
docker-compose up -d --build

# Check service status
docker-compose ps
```

---

## 📌 File List (Download These)

1. `user-service-main.py` → user-service/app/main.py
2. `order-service-main.py` → order-service/app/main.py
3. `payment-service-main.py` → payment-service/app/main.py
4. `notification-service-main.py` → notification-service/app/main.py
5. `app__init__.py` → Each service's app/__init__.py
6. `requirements-shared.txt` → Each service's requirements.txt
7. `Dockerfile-shared` → Each service's Dockerfile
8. `docker-compose-all.yml` → docker-compose.yml (root level)
9. `k8s-deployments.yaml` → k8s/deployments.yaml

---

## ✅ Quick Test Curl Commands

### User Service
```bash
# Create user
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@test.com", "phone": "1234567890"}'

# List users
curl http://localhost:8001/users

# Get user
curl http://localhost:8001/users/1
```

### Order Service
```bash
# Create order
curl -X POST http://localhost:8002/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product": "Laptop", "quantity": 2, "price": 999.99}'

# List orders
curl http://localhost:8002/orders
```

### Payment Service
```bash
# Create payment
curl -X POST http://localhost:8003/payments \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "user_id": 1, "amount": 1999.98, "method": "credit_card"}'

# List payments
curl http://localhost:8003/payments
```

### Notification Service
```bash
# Create notification
curl -X POST http://localhost:8004/notifications \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "message": "Order placed!", "type": "order"}'

# List notifications
curl http://localhost:8004/notifications
```

---

## 🔄 Service Endpoints

| Service | Port | Endpoint | Method |
|---------|------|----------|--------|
| User | 8001 | /users | GET, POST |
| User | 8001 | /users/{id} | GET, PUT, DELETE |
| Order | 8002 | /orders | GET, POST |
| Order | 8002 | /orders/{id} | GET, PUT, DELETE |
| Payment | 8003 | /payments | GET, POST |
| Payment | 8003 | /payments/{id} | GET, PUT, DELETE |
| Notification | 8004 | /notifications | GET, POST |
| Notification | 8004 | /notifications/{id} | GET, PUT, DELETE |

---

## 🚀 Next Steps After Testing

1. ✅ Test locally with docker-compose
2. ✅ Push images to Docker Hub / Azure Container Registry
3. ✅ Create Azure DevOps CI pipeline
4. ✅ Deploy to Kubernetes using k8s-deployments.yaml

---

## 📋 Summary

✅ ONE Dockerfile for all services  
✅ ONE requirements.txt for all services  
✅ docker-compose.yml runs all 4 at once  
✅ Each service independent & separate  
✅ Ready for Kubernetes deployment  

**Total files: Just 9!** 🎉

---

Done! Now just: `docker-compose up -d` 🚀
