# OS Synchronization Simulation

This project contains Python simulations comparing Dekker's algorithm, Peterson's algorithm, and Semaphore-based solutions.
It measures performance, CPU utilization, waiting time, and scalability.

## How to Run Locally

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the simulation
python main.py
```

## How to Run via Docker (Cross-Platform / Containerized)

This will ensure the application runs in a standardized Linux environment, regardless of your host OS.
```bash
docker-compose up --build
```
The output charts and diagrams will be saved cleanly into the `outputs/` directory on your host machine due to the Docker volume mapping.
