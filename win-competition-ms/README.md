# Win Competition Microservice

This microservice determines the **winner(s) for competitions**.

## Features

- Calculate and assign winners for finished competitions
- Provide winner information via API

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

| Method | Endpoint                   | Description           |
|--------|----------------------------|-----------------------|
| GET    | `/competitions/win`        | List winners          |
| POST   | `/competitions/win`        | Assign winners        |

## Docker

```bash
docker build -t win-competition-ms .
docker run -p 8004:8004 win-competition-ms
```

## License

MIT License
