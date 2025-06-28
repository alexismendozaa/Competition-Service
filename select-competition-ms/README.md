# Select Competition Microservice

This microservice manages the **selection of participants** for competitions.

## Features

- Select eligible participants for ongoing competitions
- Apply selection criteria and filters
- Expose selection data via API

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

| Method | Endpoint                   | Description                    |
|--------|----------------------------|--------------------------------|
| GET    | `/competitions/select`     | List selected participants     |
| POST   | `/competitions/select`     | Select participants for a competition |

## Docker

```bash
docker build -t select-competition-ms .
docker run -p 8002:8002 select-competition-ms
```

## License

MIT License
