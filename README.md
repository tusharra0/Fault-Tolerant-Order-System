<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Fault Tolerant Order Processing System</h3>

  <p align="center">
    A distributed, fault-tolerant microservices system for order processing built with Python, FastAPI, RabbitMQ, and PostgreSQL.
    <br />
    <a href="#about-the-project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#usage">View Demo</a>
    ·
    <a href="https://github.com/your_username/fault-tolerant-order-system/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/your_username/fault-tolerant-order-system/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The **Fault Tolerant Order Processing System** simulates a distributed e-commerce backend where customer orders pass through multiple stages:

1. **Order Service** – Accepts incoming orders via FastAPI and publishes to RabbitMQ.  
2. **Payment Service** – Consumes `order.created` events, simulates payment authorization, and publishes `payment.authorized`.  
3. **Inventory Service** – Consumes `payment.authorized`, reserves stock, and publishes `inventory.reserved`.  
4. **Shipping Service** – Consumes `inventory.reserved`, creates shipment, and publishes `shipping.ready`.  

**Fault Tolerance**  
- RabbitMQ is used with **retries** and **dead-letter queues (DLQs)** to handle service crashes or processing failures.  
- Each service has its own **PostgreSQL database** and writes its part of the order pipeline.  
- A central order DB (Postgres/RDS) provides consistency.  
- Monitoring with **CloudWatch** tracks queue depth, latency, and uptime.  

This project showcases **event-driven microservices architecture**, **resilience under failure**, and **distributed systems design**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ARCHITECTURE -->
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
