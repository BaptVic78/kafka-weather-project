CREATE TABLE IF NOT EXISTS warning_temperatures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    temperature FLOAT,
    timestamp DATETIME
)