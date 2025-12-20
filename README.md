# Real-Time Weather Data Pipeline with Apache Kafka 🌦️

## Project Description
This project implements a **containerized Big Data pipeline** simulating a real-time IoT weather monitoring system.

It demonstrates the ingestion, processing, and storage of streaming data using **Apache Kafka** as the backbone. The system consists of a Python producer (simulating sensors), a Python consumer (processing logic and alerts), and a MySQL database for persistence, all orchestrated via **Docker Compose**.

### Architecture Overview
`[Sensor Simulation] -> [Kafka Producer] -> [Kafka Cluster] -> [Kafka Consumer] -> [MySQL Database]`

---

## Technologies & Tools
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

## Installation & How to Run

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

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/BaptVic78/kafka-weather-project.git](https://github.com/BaptVic78/kafka-weather-project.git)
    cd kafka-weather-project
    ```

2.  **Start the infrastructure:**
    ```bash
    docker-compose up -d --build
    ```
    ```bash
    docker ps
    ```
    We can see our 5 containers well launched:
    ![active containers](/screenshots/containers_actives.jpg)

3.  **Check the logs:**
    ```bash
    docker-compose logs -f producer
    ```
    We can check into the terminal:
    ![producer logs](/screenshots/producer_logs.jpg)

    ```bash
    docker-compose logs -f consumer
    ```
    Here is an example of result: Each time the temperature is above the threashold of 30°C, the consumer reports an alert
    ![consumer logs](/screenshots/consumer_logs.jpg)

---

4.  **Check the Database:**
    ```bash
    docker exec -it mysql_db mysql -u root weather_db
    ```
    ```bash
    SHOW TABLES;
    ```
    After this, you should see this in the terminal:
    ![tables](/screenshots/tables.jpg)

    ```bash
    SELECT * FROM warning_temperatures;
    ```
    After this query, you should see the values in the table:
    ![warning_temperatures table](/screenshots/warning_temperatures_table.jpg)

## How this tool fits into a Big Data ecosystem

This pipeline follows the **Kappa Architecture** (Stream-only processing) and represents a modular Big Data ingestion flow.

* **Ingestion Layer (Apache Kafka):** In a real-world IoT scenario with millions of sensors, Kafka acts as a **distributed buffer**. It handles high **Velocity** and **Volume**, ensuring that data is never lost even if the database is slow or offline.
* **Processing Layer (Python Consumer):** This represents **Stream Processing**. Instead of waiting for daily batches, we analyze data "in-flight". While we use Python here, this role is typically filled by **Apache Spark** or **Flink** for massive scale.
* **Serving Layer (MySQL):** Once processed and filtered (e.g., only keeping alerts), the data is moved to a relational database. This allows Business Intelligence (BI) tools like **Grafana** or **Tableau** to query the results and display real-time dashboards.

**Summary of the flow:**
`IoT Sensors` ➡️ `Real-time Buffering (Kafka)` ➡️ `Live Analytics (Consumer)` ➡️ `Persistance (MySQL)`

## Challenges Encountered & Solutions

### 1. Docker Networking & Service Discovery
* **The Problem:** Initially, the Python scripts failed to connect to Kafka or MySQL using `localhost` because, inside a container, `localhost` refers to the container itself, not the host machine.
* **The Solution:** I updated the connection strings to use the Docker service names defined in `docker-compose.yml` (`kafka:29092` and `mysql_db`). I also configured Kafka's `ADVERTISED_LISTENERS` to distinguish between internal and external traffic.

### 2. Startup Race Conditions (Dependency Management)
* **The Problem:** The Python scripts were starting faster than the Kafka broker and MySQL server. This caused the scripts to crash immediately with `NoBrokersAvailable` or `ConnectionRefused` errors.
* **The Solution:** Instead of just using `depends_on`, I implemented a **Retry Logic** in the Python code using `while` loops and `try/except` blocks. The scripts now wait and retry the connection every 5 seconds until the services are fully operational.

### 3. Data Type Mismatch (Python vs SQL)
* **The Problem:** The Producer was sending Unix timestamps as floats, which caused "Data truncated" errors in MySQL as the table expected a specific `DATETIME` format.
* **The Solution:** I used Python's `datetime` library to format the timestamps into a SQL-friendly string (`%Y-%m-%d %H:%M:%S`) before sending them through Kafka.

### 4. GitHub Authentication (WSL to Remote)
* **The Problem:** When pushing the code from the WSL terminal, GitHub rejected the account password due to the removal of password authentication in 2021.
* **The Solution:** I generated a **Personal Access Token (PAT)** on GitHub and used it as the password in the terminal. I also configured the local Git identity (`user.name` and `user.email`) to allow the commit process.

### 5. Persistent Storage Permissions
* **The Problem:** Using a bind mount for MySQL data on a Windows/WSL filesystem caused permission conflicts, preventing the database from initializing.
* **The Solution:** I switched to **Docker Named Volumes** (`db_data`), allowing Docker to manage the Linux-native filesystem permissions internally and ensuring data persistence between restarts.

## Project Structure

```text
kafka-weather-project/
├── docker-compose.yml   # Infrastructure orchestration (Kafka, Zookeeper, MySQL)
├── Dockerfile           # Python environment setup (used by producer & consumer)
├── requirements.txt     # Python dependencies (kafka-python-ng, mysql-connector)
├── init.sql             # SQL script to initialize the weather_db schema
├── producer.py          # Script: Generates random weather data & sends to Kafka
├── consumer.py          # Script: Reads from Kafka, filters alerts & saves to MySQL
├── .gitignore           # Tells Git to ignore venv/, __pycache__ and temp files
├── README.md            # Complete project documentation & technical report
└── screenshots/         # Folder containing sample output & execution proof
    ├── containers_actives.jpg
    ├── producer_logs.jpg
    ├── consumer_logs.jpg
    ├── tables.jpg
    ├── warning_temperatures_table.jpg
```