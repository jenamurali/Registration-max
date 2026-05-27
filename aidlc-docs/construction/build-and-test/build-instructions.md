# Build Instructions

## Prerequisites
- Python 3.12+
- SQL Server (for production) or SQLite (for dev/test)
- pip

## Build Steps

### 1. Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create `.env` file:
```env
DATABASE_URL=mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+17+for+SQL+Server
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
LOG_FORMAT=text
```

### 4. Run the Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Verify
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/events (returns events list)
