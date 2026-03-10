# SQLite Metadata Backend

A FastAPI-based backend service for extracting and serving SQLite database metadata.

## Features

- Extract database table information
- Get table schemas, columns, and constraints
- Retrieve indexes and foreign keys
- Complete database metadata overview
- RESTful API endpoints

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Navigate to the backend directory:
```bash
cd sqlite-metadata-backend
```

2. Create and activate a virtual environment:
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
# python -m venv venv
# source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create the sample database:
```bash
python app/utils/create_sample_db.py
```

## Running the Server

### Development Mode

```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --port 5000
```

The API will be available at: `http://localhost:5000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

### Available Endpoints

- `GET /health` - Health check endpoint
- `GET /api/metadata/tables` - Get all tables
- `GET /api/metadata/tables/{table_name}/schema` - Get table schema
- `GET /api/metadata/tables/{table_name}/indexes` - Get table indexes
- `GET /api/metadata/tables/{table_name}/foreign-keys` - Get foreign keys
- `GET /api/metadata/database` - Get complete database metadata

## Project Structure

```
sqlite-metadata-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main application entry point
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── metadata_controller.py  # Database metadata logic
│   ├── routes/
│   │   ├── __init__.py
│   │   └── metadata.py        # API route definitions
│   └── utils/
│       ├── __init__.py
│       └── create_sample_db.py  # Sample database generator
├── database/
│   └── sqlite_test            # SQLite test database
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
└── run.py                     # Server startup script
```

## Environment Variables

Edit the `.env` file to configure:

```
PORT=5000
DB_PATH=./database/sqlite_test
NODE_ENV=development
```

## Testing

To test the API endpoints, you can use:
- The built-in Swagger UI at `/docs`
- curl commands
- Postman or similar tools

Example curl command:
```bash
curl http://localhost:5000/api/metadata/tables
```

## Using Your Own Database

To use your own SQLite database instead of the sample:

1. Place your `.db` file in the `database/` directory
2. Update the `DB_PATH` in `.env`:
```
DB_PATH=./database/your-database.db
```
3. Restart the server

## Troubleshooting

**Port already in use:**
- Change the PORT in `.env` file
- Or kill the process using the port

**Database connection errors:**
- Verify the database file exists
- Check file permissions
- Ensure the path in `.env` is correct

**CORS issues:**
- CORS is configured to allow all origins in development
- For production, update `allow_origins` in `app/main.py`
