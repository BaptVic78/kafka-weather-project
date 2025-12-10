# Real-Time Weather Data Pipeline with Apache Kafka 🌦️

## 📝 Project Description
This project implements a **containerized Big Data pipeline** simulating a real-time IoT weather monitoring system.

It demonstrates the ingestion, processing, and storage of streaming data using **Apache Kafka** as the backbone. The system consists of a Python producer (simulating sensors), a Python consumer (processing logic and alerts), and a MySQL database for persistence, all orchestrated via **Docker Compose**.

### Architecture Overview
`[Sensor Simulation] -> [Kafka Producer] -> [Kafka Cluster] -> [Kafka Consumer] -> [MySQL Database]`

---

## 🛠️ Technologies & Tools
* **Infrastructure:** Docker & Docker Compose
* **Streaming Engine:** Apache Kafka (Confluent Image) & Zookeeper
* **Database:** MySQL 8.0
* **Logic:** Python 3.12 (using `kafka-python-ng` and `mysql-connector-python`)

### Why Apache Kafka?
I selected **Apache Kafka** for this project because it is the industry standard for building real-time streaming data pipelines.
1.  **Decoupling:** It separates the data generation (Producer) from the processing (Consumer).
2.  **Scalability:** Unlike simple queues, Kafka is distributed and can handle massive throughput.
3.  **Persistence:** Data is stored on disk, ensuring no data loss even if the consumer is temporarily down.

---

## 🚀 Installation & How to Run

### Prerequisites
* Docker Desktop installed and running.
* Git.

### Steps
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/BaptVic78/kafka-weather-project.git](https://github.com/BaptVic78/kafka-weather-project.git)
    cd kafka-weather-project
    ```

2.  **Start the infrastructure:**
    This command builds the custom Python images and starts Zookeeper, Kafka, and MySQL.
    ```bash
    docker-compose up -d --build
    ```

3.  **Verify Execution (Logs):**
    To see the pipeline in action (data flowing from producer to consumer):
    ```bash
    docker-compose logs -f producer consumer
    ```
    *You should see "✅ Message Sent" and "⚠️ Alert Saved" logs.*

4.  **Check the Database:**
    To verify that alerts are actually stored:
    ```bash
    docker exec -it mysql_db mysql -u root weather_db -e "SELECT * FROM warning_temperatures;"
    ```

## Working example

1.  **Start the infrastructure:**
    ```bash
    docker-compose up -d --build
    ```
    ```bash
    docker ps
    ```
    *We can see our 5 containers well launched:*
    ![active containers](/screenshots/containers_actives.jpg)

2.  **Check the logs of producer to see if it send values:**
    ```bash
    docker-compose logs -f producer
    ```
    *We can check into the terminal:*
    ![producer logs](/screenshots/producer_logs.jpg)

---

## 📂 Project Structure

```text
kafka-weather-project/
├── docker-compose.yml   # Orchestration of all services
├── Dockerfile           # Blueprint for Python images
├── requirements.txt     # Python dependencies
├── init.sql             # Database initialization script
├── producer.py          # Data generation script
├── consumer.py          # Processing and Alerting script
└── README.md            # Documentation