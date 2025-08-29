# Cohezy

A modern web application with a FastAPI backend and a static frontend, designed for user/session management and extensibility.

## Features
- FastAPI backend (Python 3.11)
- SQLAlchemy ORM, PostgreSQL database
- User authentication (JWT)
- User/session management APIs
- Dockerized for easy deployment
- Swagger/OpenAPI documentation

## Project Structure
```
Cohezy/
├── backend/
│   ├── src/
│   │   ├── api/           # FastAPI routers & endpoints
│   │   ├── config/        # Settings, DB, Redis config
│   │   ├── core/          # Core logic (logger, security, celery)
│   │   ├── db/            # DB session, base, init
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utilities
│   ├── main.py            # FastAPI app entrypoint
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend Dockerfile
├── frontend/
│   ├── index.html         # Static frontend
│   ├── scripts/           # JS
│   ├── styles/            # CSS
│   └── Dockerfile         # Frontend Dockerfile
├── docker-compose.yml     # Multi-service orchestration
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.11+ for local dev

### Quick Start (Docker)
```sh
git clone https://github.com/teekayyj-dotcom/Cohezy.git
cd Cohezy
docker compose up --build
```
- Backend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Frontend: http://localhost:8080

### Local Development
1. Copy `.env.example` to `.env` and update settings.
2. Install Python dependencies:
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
3. Run FastAPI app:
   ```sh
   uvicorn main:app --reload
   ```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## License
MIT
