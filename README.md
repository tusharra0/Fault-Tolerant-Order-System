# Fault Tolerant Order Processing System

A distributed, fault tolerant microservices system for order processing built with **Python, FastAPI, RabbitMQ, and PostgreSQL**. It’s designed to handle orders through events, keep working even if a service fails, and scale like a real distributed system.

---

## About the Project

The system simulates an e-commerce backend where customer orders pass through multiple stages:

1. **Order Service** – Accepts incoming orders via FastAPI and publishes to RabbitMQ.  
2. **Payment Service** – Consumes `order.created`, simulates payment authorization, and publishes `payment.authorized`.  
3. **Inventory Service** – Consumes `payment.authorized`, reserves stock, and publishes `inventory.reserved`.  
4. **Shipping Service** – Consumes `inventory.reserved`, creates shipments, and publishes `shipping.ready`.  

### Fault Tolerance
- RabbitMQ queues are **durable** and configured with **Dead Letter Queues**.  
- Failed messages are retried and eventually routed to a DLQ if recovery isn’t possible.  
- Each service has its own **PostgreSQL database**, ensuring data consistency and isolation.  
- Monitoring is supported via **CloudWatch** to track queue depth, latency, and uptime.  

---

## Architecture

```mermaid
flowchart TD
    A[Client API] -->|POST /orders| B[Order Service]
    B -->|order.created| Q((RabbitMQ Exchange))
    Q -->|payment.authorized| P[Payment Service]
    Q -->|inventory.reserved| I[Inventory Service]
    Q -->|shipping.ready| S[Shipping Service]

    P -->|writes| PDB[(Payments DB)]
    I -->|writes| IDB[(Inventory DB)]
    S -->|writes| SDB[(Shipping DB)]
    B -->|writes| ODB[(Central Orders DB)]

```


## Tech Stack

- **Language:** Python 3.11  
- **Framework:** FastAPI  
- **Message Broker:** RabbitMQ  
- **Database:** PostgreSQL (locally) / Amazon RDS (cloud)  
- **Deployment:** Docker Compose (locally), AWS EC2 (cloud)  
- **Monitoring:** AWS CloudWatch  
- **Testing:** Pytest, Locust (load testing)  

---

##  Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)  

### Installation
1. Clone the repo:
   ```sh
   git clone https://github.com/your_username/fault-tolerant-order-system.git
   cd fault-tolerant-order-system
2. Start all services:
   ```sh
   docker-compose up --build
3. Verify services
   ```sh
   Order API: http://localhost:8000/orders
   RabbitMQ Dashboard: http://localhost:15672
---

##  Usage

### Submit a new order

```bash
curl -X POST "http://localhost:8000/orders" \
     -H "Content-Type: application/json" \
     -d '{
           "order_id": "123",
           "user_id": "42",
           "items": ["Book"],
           "total": 20.0
         }'
```
### Simulating a failure 
```bash
curl -X POST "http://localhost:8000/orders" \
     -H "Content-Type: application/json" \
     -d '{
           "order_id": "999",
           "user_id": "42",
           "items": ["Laptop"],
           "total": 2000,
           "force_fail": true
         }'
```
## Deployment & Monitoring

- **Order API (FastAPI Docs):** [http://3.80.195.219:8000/docs](http://3.80.195.219:8000/docs)  
- **RabbitMQ Dashboard:** [http://3.80.195.219:15672](http://3.80.195.219:15672)  
- **CloudWatch Metrics Dashboard:** [Your Public Link Here]  

---
## Roadmap

- [x] Core Order → Payment → Inventory → Shipping pipeline  
- [x] Retry logic + DLQ for fault tolerance  
- [x] Docker Compose local setup  
- [X] AWS EC2 + RDS deployment  
- [X] CI/CD pipeline with GitHub Actions  
- [X] Grafana dashboard for monitoring  

---
## 📬 Contact

- **Tushar Rao** – [LinkedIn](https://www.linkedin.com/in/tusharra0/)  
- **Steric Tsui** – [LinkedIn](https://www.linkedin.com/in/steric-tsui/)  
