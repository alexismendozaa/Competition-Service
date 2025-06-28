# History Competition Microservice

This microservice provides **access to competition history and past results**.

## Features

- Retrieve past competitions
- Search and filter historical results
- Provide analytics-ready data

## Technology Stack

- Python 3.9+
- Flask (or FastAPI/Django)
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

| Method | Endpoint                     | Description                |
|--------|------------------------------|----------------------------|
| GET    | `/competitions/history`      | List historical competitions |

## Docker

```bash
docker build -t history-competition-ms .
docker run -p 8005:8005 history-competition-ms
```

## License

MIT License
