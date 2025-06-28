# End Competition Microservice

This microservice handles **finishing competitions** and updating their status in the SneakRush platform.

## Features

- End a competition
- Update the status of ongoing competitions
- Notify other services about the competition outcome

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

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | `/competitions/end`   | End a competition          |

## Docker

```bash
docker build -t end-competition-ms .
docker run -p 8003:8003 end-competition-ms
```

## License

MIT License
