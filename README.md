# OrderFlow

**OrderFlow** is a local-first, production-inspired **microservices reference architecture** designed for hands-on learning, system design practice, and technical interviews.
The project demonstrates how independently deployed services communicate through an **API Gateway**, and how a modern **frontend** consumes backend capabilities in a clean, scalable way — *without Docker or Kubernetes*, to keep the focus on architecture and behavior.

---

## 🎯 Purpose & Scope

OrderFlow is intentionally **simple but realistic**:

* Models real-world service boundaries (Customers, Orders)
* Enforces a single entry point via an API Gateway
* Separates frontend concerns from backend domains
* Runs entirely on a local machine for fast iteration

It is ideal for:

* Understanding microservices fundamentals
* Practicing system design explanations
* Demonstrating architectural thinking in interviews
* Serving as a base for future Docker / Kubernetes migration

---

## 🏛️ High-Level Architecture

```mermaid
graph LR
    U[User Browser]
    U --> F[Frontend (React + Vite)]
    F --> G[API Gateway (FastAPI)]
    G --> C[Customer Service]
    G --> O[Order Service]
```

### Architectural Principles

* **Single Responsibility** – each service owns a single business domain
* **Loose Coupling** – services communicate only via HTTP APIs
* **API Gateway Pattern** – frontend never talks directly to backend services
* **Stateless Services** – in-memory data for simplicity and resetability

---

## 🧩 System Components

### 1️⃣ Frontend (UI Layer)

**Technology:** React, TypeScript, Vite
**Port:** `5173`

**Responsibilities:**

* Provides a user-facing dashboard
* Sends HTTP requests to the API Gateway only
* Displays aggregated data from multiple services

The frontend is **fully decoupled** from backend service topology. It knows nothing about Customer or Order services directly.

---

### 2️⃣ API Gateway (Integration Layer)

**Technology:** Python, FastAPI
**Port:** `8000`

**Responsibilities:**

* Acts as the **single entry point** for the frontend
* Routes requests to the appropriate backend service
* Aggregates and normalizes APIs
* Shields the frontend from internal service changes

This component is the backbone of the system and represents how real production systems expose APIs.

---

### 3️⃣ Customer Service (Domain Service)

**Technology:** Python, FastAPI
**Port:** `8001`

**Responsibilities:**

* Manages customer entities
* Handles creation and retrieval of customers
* Owns all customer-related business logic

The service is **independent** and can evolve without impacting other services.

---

### 4️⃣ Order Service (Domain Service)

**Technology:** Python, FastAPI
**Port:** `8002`

**Responsibilities:**

* Manages orders and order lifecycle
* Handles creation and retrieval of orders
* Owns order-related business rules

---

## 🔗 Communication Flow

1. User interacts with the **Frontend UI**
2. Frontend sends HTTP requests to the **API Gateway**
3. API Gateway routes requests:

   * Customer-related → Customer Service
   * Order-related → Order Service
4. Responses propagate back through the Gateway to the Frontend

This mirrors real-world distributed systems behavior.

---

## 🚀 Running the System Locally

### Prerequisites

* **Python 3.9+**
* **Node.js 18+**

Each component runs in its **own terminal** to emphasize service independence.

### Start Customer Service

```bash
cd services/customer
pip install -r requirements.txt
uvicorn main:app --port 8001 --reload
```

### Start Order Service

```bash
cd services/order
pip install -r requirements.txt
uvicorn main:app --port 8002 --reload
```

### Start API Gateway

```bash
cd services/api-gateway
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
```

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 API Access

**Gateway Swagger UI:**
[http://localhost:8000/docs](http://localhost:8000/docs)

### Public Endpoints

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/healthz`       | Gateway health check |
| GET    | `/api/customers` | List customers       |
| POST   | `/api/customers` | Create customer      |
| GET    | `/api/orders`    | List orders          |
| POST   | `/api/orders`    | Create order         |

---

## 📁 Repository Structure

```
order_flow/
├── frontend/              # React + TypeScript UI
├── services/
│   ├── api-gateway/       # API Gateway
│   ├── customer/          # Customer service
│   └── order/             # Order service
├── ingress-orderflow.yaml # (Future K8s ingress)
└── README.md              # Documentation
```

---

## 🧠 Design Notes

* No database is used intentionally (in-memory state)
* Each service can be containerized independently later
* API Gateway makes Kubernetes / Docker migration trivial
* Architecture scales naturally to auth, payments, inventory, etc.

---

## 🛣️ Next Evolution Steps (Optional)

* Dockerize each service
* Introduce persistent storage (PostgreSQL / Redis)
* Add authentication (JWT)
* Deploy to Kubernetes with Ingress
* Add CI/CD pipelines

---

**OrderFlow** is not a demo app — it is a **thinking framework** for building and explaining distributed systems.

---

## 🧪 Testing Strategy

The project includes a comprehensive testing layer designed to ensure reliability across microservices.

### Types of Tests
1. **Unit Tests**: Verify internal business logic and state management (e.g., creating orders, managing customer lists).
2. **API Tests**: Validate HTTP endpoints, response schemas, and status codes using `TestClient`.
3. **Data Consistency Tests**: Ensure in-memory data structures are correctly updated and persisted during the application lifecycle.

### Folder Structure
Each service contains a dedicated `tests/` directory:
```
services/
  customer/tests/   # Customer service tests
  order/tests/      # Order service tests
  api-gateway/tests/# Integration/Mock tests
```

### Running Tests
You can run tests for individual services or the entire project.

**Run Tests:**
```bash
# Run separately to avoid module name conflicts
python -m pytest services/customer/tests
python -m pytest services/order/tests
python -m pytest services/api-gateway/tests
```

**Why this strategy?**
* **Isolation**: Each service is tested independently, mimicking a real microservices pipeline.
* **Speed**: In-memory data allowing for fast test execution without database setup.
* **Reliability**: API Gateway tests use mocking (`respx`) to simulate downstream services, ensuring stability even if other services are offline.
