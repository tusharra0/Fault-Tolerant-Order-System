## 🏗️ Architecture

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
