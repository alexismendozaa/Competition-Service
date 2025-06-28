# Start Competition Microservice

This microservice is responsible for **creating and initializing new competitions** in the SneakRush platform.

## Features

- Create a new competition
- Initialize competition parameters and participants
- Validate input data for new competitions

## Technology Stack

- Python 3.9+
- Flask (or FastAPI/Django, depending on implementation)
- REST API

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Configure environment variables in a `.env` file if required.

3. Run the service:
    ```bash
    python app.py
    ```

## API Endpoints

| Method | Endpoint               | Description            |
|--------|------------------------|------------------------|
| POST   | `/competitions/start`  | Create a new competition |

## Docker

```bash
docker build -t start-competition-ms .
docker run -p 8001:8001 start-competition-ms
```

## License

MIT License
