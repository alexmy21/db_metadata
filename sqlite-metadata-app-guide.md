# SQLite Database Metadata Viewer - Step-by-Step Guide

A complete guide to building a professional React application that interacts with a backend API to display SQLite database metadata information.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Backend Setup (Node.js + Express)](#backend-setup)
4. [Frontend Setup (React)](#frontend-setup)
5. [Professional UI Implementation](#professional-ui-implementation)
6. [API Integration](#api-integration)
7. [Testing & Deployment](#testing--deployment)

---

## Project Overview

### Architecture
- **Frontend**: React with Material-UI / Tailwind CSS for professional UI
- **Backend**: Python + FastAPI/Flask
- **Database**: SQLite with metadata extraction
- **Communication**: RESTful API

### Features
- View database tables and structure
- Display column information (name, type, constraints)
- Show indexes and foreign keys
- Table relationships visualization
- Query statistics

---

## Prerequisites

Ensure you have the following installed:
- Python (v3.8 or higher)
- pip (Python package manager)
- Code editor (VS Code recommended)
- Git (optional)

---

## Backend Setup

### Step 1: Initialize Backend Project

```bash
# Create backend directory
mkdir sqlite-metadata-backend
cd sqlite-metadata-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlite3 python-dotenv pydantic
# Or for Flask:
# pip install flask flask-cors python-dotenv
```

### Step 2: Create Backend Structure

```bash
# Create directory structure
mkdir app
mkdir app/routes
mkdir app/controllers
mkdir app/utils
mkdir database

# Create requirements.txt
echo fastapi==0.109.0 > requirements.txt
echo uvicorn==0.27.0 >> requirements.txt
echo python-dotenv==1.0.0 >> requirements.txt
echo pydantic==2.6.0 >> requirements.txt
```

### Step 3: Configure Backend Server

Create `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.routes import metadata

load_dotenv()

app = FastAPI(
    title="SQLite Metadata API",
    description="API for extracting SQLite database metadata",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(metadata.router, prefix="/api/metadata", tags=["metadata"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
```

### Step 4: Implement Database Controller

Create `app/controllers/metadata_controller.py`:

```python
import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import HTTPException

class MetadataController:
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(__file__), 
                                       '../../database/sample.db')
        else:
            self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    
    def get_tables(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tables in the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """
        
        try:
            cursor.execute(query)
            tables = [dict(row) for row in cursor.fetchall()]
            return {"tables": tables}
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get schema for a specific table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f"PRAGMA table_info({table_name});"
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            columns = []
            for row in rows:
                columns.append({
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "notNull": row[3] == 1,
                    "defaultValue": row[4],
                    "primaryKey": row[5] == 1
                })
            
            return {
                "tableName": table_name,
                "columns": columns
            }
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_indexes(self, table_name: str) -> Dict[str, Any]:
        """Get indexes for a specific table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f"PRAGMA index_list({table_name});"
        
        try:
            cursor.execute(query)
            indexes = [dict(row) for row in cursor.fetchall()]
            return {
                "tableName": table_name,
                "indexes": indexes
            }
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_foreign_keys(self, table_name: str) -> Dict[str, Any]:
        """Get foreign keys for a specific table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f"PRAGMA foreign_key_list({table_name});"
        
        try:
            cursor.execute(query)
            foreign_keys = [dict(row) for row in cursor.fetchall()]
            return {
                "tableName": table_name,
                "foreignKeys": foreign_keys
            }
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_database_metadata(self) -> Dict[str, Any]:
        """Get complete database metadata"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table_query = """
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%';
        """
        
        try:
            cursor.execute(table_query)
            tables = cursor.fetchall()
            
            metadata = {
                "databaseName": Path(self.db_path).name,
                "tableCount": len(tables),
                "tables": []
            }
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                metadata["tables"].append({
                    "name": table_name,
                    "columnCount": len(columns),
                    "columns": [dict(col) for col in columns]
                })
            
            return metadata
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

# Create single instance
metadata_controller = MetadataController()
```

### Step 5: Create API Routes

Create `app/routes/metadata.py`:

```python
from fastapi import APIRouter, Path
from app.controllers.metadata_controller import metadata_controller

router = APIRouter()

@router.get("/tables")
async def get_tables():
    """Get all tables in the database"""
    return metadata_controller.get_tables()

@router.get("/tables/{table_name}/schema")
async def get_table_schema(
    table_name: str = Path(..., description="Name of the table")
):
    """Get schema for a specific table"""
    return metadata_controller.get_table_schema(table_name)

@router.get("/tables/{table_name}/indexes")
async def get_indexes(
    table_name: str = Path(..., description="Name of the table")
):
    """Get indexes for a specific table"""
    return metadata_controller.get_indexes(table_name)

@router.get("/tables/{table_name}/foreign-keys")
async def get_foreign_keys(
    table_name: str = Path(..., description="Name of the table")
):
    """Get foreign keys for a specific table"""
    return metadata_controller.get_foreign_keys(table_name)

@router.get("/database")
async def get_database_metadata():
    """Get complete database metadata"""
    return metadata_controller.get_database_metadata()
```

Create `app/__init__.py` (empty file to make it a package):

```python
# Empty file
```

Create `app/routes/__init__.py` (empty file):

```python
# Empty file
```

Create `app/controllers/__init__.py` (empty file):

```python
# Empty file
```

### Step 6: Create Sample Database

Create `app/utils/create_sample_db.py`:

```python
import sqlite3
import os
from pathlib import Path

def create_sample_database():
    """Create a sample SQLite database with tables"""
    # Ensure database directory exists
    db_dir = Path(__file__).parent.parent.parent / 'database'
    db_dir.mkdir(exist_ok=True)
    
    db_path = db_dir / 'sample.db'
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            published BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create Comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
    """)
    
    # Insert sample data
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, email) VALUES 
        ('john_doe', 'john@example.com'),
        ('jane_smith', 'jane@example.com')
    """)
    
    cursor.execute("""
        INSERT OR IGNORE INTO posts (user_id, title, content, published) VALUES 
        (1, 'First Post', 'This is my first post', 1),
        (2, 'Another Post', 'Hello world', 1)
    """)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f'Sample database created successfully at {db_path}')

if __name__ == '__main__':
    create_sample_database()
```

Create `app/utils/__init__.py` (empty file):

```python
# Empty file
```

### Step 7: Create Run Scripts

Create `run.py` in the root directory:

```python
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    load_dotenv()
    port = int(os.getenv("PORT", 5000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
```

### Step 8: Create .env File

Create `.env`:

```
PORT=5000
DB_PATH=./database/sample.db
NODE_ENV=development
```

### Step 9: Run Backend

```bash
# Create sample database
python app/utils/create_sample_db.py

# Start development server
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --port 5000
```

---

## Frontend Setup

### Step 1: Create React Application

```bash
# Navigate to project root
cd ..

# Create React app with Vite (recommended) or Create React App
npm create vite@latest sqlite-metadata-frontend -- --template react
cd sqlite-metadata-frontend

# Install dependencies
npm install

# Install UI library (choose one)
# Option 1: Material-UI
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material

# Option 2: Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install additional dependencies
npm install axios react-router-dom
```

### Step 2: Project Structure

```bash
src/
├── components/
│   ├── DatabaseOverview.jsx
│   ├── TableList.jsx
│   ├── TableDetails.jsx
│   ├── ColumnInfo.jsx
│   ├── Sidebar.jsx
│   └── Header.jsx
├── services/
│   └── api.js
├── hooks/
│   └── useMetadata.js
├── styles/
│   └── App.css
├── App.jsx
└── main.jsx
```

---

## Professional UI Implementation

### Step 1: Configure API Service

Create `src/services/api.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const metadataAPI = {
  // Get all tables
  getTables: () => api.get('/metadata/tables'),
  
  // Get table schema
  getTableSchema: (tableName) => 
    api.get(`/metadata/tables/${tableName}/schema`),
  
  // Get table indexes
  getIndexes: (tableName) => 
    api.get(`/metadata/tables/${tableName}/indexes`),
  
  // Get foreign keys
  getForeignKeys: (tableName) => 
    api.get(`/metadata/tables/${tableName}/foreign-keys`),
  
  // Get complete database metadata
  getDatabaseMetadata: () => 
    api.get('/metadata/database'),
};

export default api;
```

### Step 2: Create Custom Hook

Create `src/hooks/useMetadata.js`:

```javascript
import { useState, useEffect } from 'react';
import { metadataAPI } from '../services/api';

export const useMetadata = () => {
  const [tables, setTables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    try {
      setLoading(true);
      const response = await metadataAPI.getTables();
      setTables(response.data.tables);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { tables, loading, error, refetch: fetchTables };
};
```

### Step 3: Create Header Component (Material-UI)

Create `src/components/Header.jsx`:

```javascript
import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import StorageIcon from '@mui/icons-material/Storage';

const Header = () => {
  return (
    <AppBar position="static" elevation={0}>
      <Toolbar>
        <StorageIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          SQLite Metadata Viewer
        </Typography>
        <Typography variant="body2" color="inherit" sx={{ opacity: 0.8 }}>
          Database Explorer
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
```

### Step 4: Create Database Overview Component

Create `src/components/DatabaseOverview.jsx`:

```javascript
import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Grid, 
  Box,
  CircularProgress 
} from '@mui/material';
import { metadataAPI } from '../services/api';

const DatabaseOverview = () => {
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetadata();
  }, []);

  const fetchMetadata = async () => {
    try {
      const response = await metadataAPI.getDatabaseMetadata();
      setMetadata(response.data);
    } catch (error) {
      console.error('Error fetching metadata:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Database Overview
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Database Name
              </Typography>
              <Typography variant="h5">
                {metadata?.databaseName || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Tables
              </Typography>
              <Typography variant="h5">
                {metadata?.tableCount || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Columns
              </Typography>
              <Typography variant="h5">
                {metadata?.tables.reduce((acc, t) => acc + t.columnCount, 0) || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DatabaseOverview;
```

### Step 5: Create Table List Component

Create `src/components/TableList.jsx`:

```javascript
import React from 'react';
import { 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemText, 
  Paper,
  Typography,
  Box,
  Chip
} from '@mui/material';
import TableChartIcon from '@mui/icons-material/TableChart';

const TableList = ({ tables, selectedTable, onSelectTable }) => {
  return (
    <Paper elevation={2} sx={{ height: '100%', overflow: 'auto' }}>
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6">Tables</Typography>
      </Box>
      
      <List>
        {tables.map((table) => (
          <ListItem key={table.name} disablePadding>
            <ListItemButton
              selected={selectedTable === table.name}
              onClick={() => onSelectTable(table.name)}
            >
              <TableChartIcon sx={{ mr: 2, color: 'primary.main' }} />
              <ListItemText 
                primary={table.name}
                secondary={`${table.columnCount || ''} columns`}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default TableList;
```

### Step 6: Create Table Details Component

Create `src/components/TableDetails.jsx`:

```javascript
import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Tabs,
  Tab
} from '@mui/material';
import { metadataAPI } from '../services/api';

const TableDetails = ({ tableName }) => {
  const [schema, setSchema] = useState(null);
  const [indexes, setIndexes] = useState([]);
  const [foreignKeys, setForeignKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    if (tableName) {
      fetchTableDetails();
    }
  }, [tableName]);

  const fetchTableDetails = async () => {
    setLoading(true);
    try {
      const [schemaRes, indexesRes, fkRes] = await Promise.all([
        metadataAPI.getTableSchema(tableName),
        metadataAPI.getIndexes(tableName),
        metadataAPI.getForeignKeys(tableName)
      ]);
      
      setSchema(schemaRes.data);
      setIndexes(indexesRes.data.indexes);
      setForeignKeys(fkRes.data.foreignKeys);
    } catch (error) {
      console.error('Error fetching table details:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        {tableName}
      </Typography>

      <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)} sx={{ mb: 2 }}>
        <Tab label="Columns" />
        <Tab label="Indexes" />
        <Tab label="Foreign Keys" />
      </Tabs>

      {activeTab === 0 && (
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Column Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Constraints</TableCell>
                <TableCell>Default Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {schema?.columns.map((column) => (
                <TableRow key={column.id}>
                  <TableCell>
                    <strong>{column.name}</strong>
                  </TableCell>
                  <TableCell>
                    <Chip label={column.type} size="small" color="primary" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    {column.primaryKey && <Chip label="PK" size="small" color="success" sx={{ mr: 1 }} />}
                    {column.notNull && <Chip label="NOT NULL" size="small" color="warning" />}
                  </TableCell>
                  <TableCell>{column.defaultValue || '-'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {activeTab === 1 && (
        <Box>
          {indexes.length > 0 ? (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Index Name</TableCell>
                    <TableCell>Unique</TableCell>
                    <TableCell>Origin</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {indexes.map((index, i) => (
                    <TableRow key={i}>
                      <TableCell>{index.name}</TableCell>
                      <TableCell>
                        {index.unique ? 
                          <Chip label="Yes" size="small" color="success" /> : 
                          <Chip label="No" size="small" />
                        }
                      </TableCell>
                      <TableCell>{index.origin}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          ) : (
            <Typography color="textSecondary">No indexes found</Typography>
          )}
        </Box>
      )}

      {activeTab === 2 && (
        <Box>
          {foreignKeys.length > 0 ? (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Column</TableCell>
                    <TableCell>References</TableCell>
                    <TableCell>On Update</TableCell>
                    <TableCell>On Delete</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {foreignKeys.map((fk, i) => (
                    <TableRow key={i}>
                      <TableCell>{fk.from}</TableCell>
                      <TableCell>
                        {fk.table}.{fk.to}
                      </TableCell>
                      <TableCell>{fk.on_update}</TableCell>
                      <TableCell>{fk.on_delete}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          ) : (
            <Typography color="textSecondary">No foreign keys found</Typography>
          )}
        </Box>
      )}
    </Paper>
  );
};

export default TableDetails;
```

### Step 7: Create Main App Component

Create `src/App.jsx`:

```javascript
import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box, Container, Grid, CssBaseline } from '@mui/material';
import Header from './components/Header';
import DatabaseOverview from './components/DatabaseOverview';
import TableList from './components/TableList';
import TableDetails from './components/TableDetails';
import { useMetadata } from './hooks/useMetadata';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  const { tables, loading, error } = useMetadata();
  const [selectedTable, setSelectedTable] = useState(null);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header />
        
        <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          <DatabaseOverview />
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <TableList
                tables={tables}
                selectedTable={selectedTable}
                onSelectTable={setSelectedTable}
              />
            </Grid>
            
            <Grid item xs={12} md={8}>
              {selectedTable ? (
                <TableDetails tableName={selectedTable} />
              ) : (
                <Box
                  sx={{
                    height: '400px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    bgcolor: 'background.paper',
                    borderRadius: 1,
                  }}
                >
                  Select a table to view details
                </Box>
              )}
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
```

### Step 8: Update main.jsx

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

## API Integration

### Best Practices

1. **Error Handling**: Implement proper error handling in API calls
2. **Loading States**: Show loading indicators during API requests
3. **Caching**: Consider implementing caching for frequently accessed data
4. **Authentication**: Add JWT tokens for secure API access (optional)
5. **API Versioning**: Use versioned API endpoints (/api/v1/)

### Example Error Handling

```javascript
const fetchWithErrorHandling = async (apiCall) => {
  try {
    const response = await apiCall();
    return { data: response.data, error: null };
  } catch (error) {
    return {
      data: null,
      error: error.response?.data?.message || error.message
    };
  }
};
```

---

## Testing & Deployment

### Backend Testing

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Create test file: tests/test_metadata.py
# Run tests
pytest
```

Create `tests/test_metadata.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_get_tables():
    response = client.get("/api/metadata/tables")
    assert response.status_code == 200
    assert "tables" in response.json()

def test_get_database_metadata():
    response = client.get("/api/metadata/database")
    assert response.status_code == 200
    assert "databaseName" in response.json()
    assert "tableCount" in response.json()
```

### Frontend Testing

```bash
# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm run test
```

### Production Build

**Backend:**
```bash
# Set environment to production
# On Windows:
set ENVIRONMENT=production
python run.py

# On macOS/Linux:
# export ENVIRONMENT=production
# python run.py

# Or use gunicorn for production (Linux/macOS)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
```

**Frontend:**
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Deployment Options

1. **Backend**: Deploy to Heroku, Railway, or AWS EC2
2. **Frontend**: Deploy to Vercel, Netlify, or GitHub Pages
3. **Full Stack**: Use Docker containers with docker-compose

### Docker Setup (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./sqlite-metadata-backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./database:/app/database

  frontend:
    build: ./sqlite-metadata-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

## Additional Enhancements

### 1. Add Search Functionality
- Search tables by name
- Filter columns by type
- Search within table data

### 2. Data Visualization
- Entity-relationship diagrams
- Table size charts
- Column type distribution

### 3. Export Features
- Export schema as JSON/SQL
- Generate documentation
- Database diagram export

### 4. Advanced Features
- Query builder interface
- Real-time data preview
- Schema comparison tool
- Migration history tracking

---

## Troubleshooting

### Common Issues

**CORS Errors:**
```python
# Update CORS settings in app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Database Connection Issues:**
- Verify database file path is correct
- Check file permissions
- SQLite3 is included with Python (no separate installation needed)
- Verify virtual environment is activated

**API Connection Failed:**
- Verify backend server is running
- Check API_BASE_URL in frontend
- Confirm port numbers match

---

## Resources

- [React Documentation](https://react.dev/)
- [Material-UI](https://mui.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Uvicorn](https://www.uvicorn.org/)

---

## Conclusion

You now have a complete guide to building a professional SQLite metadata viewer application. The application features:

✅ Modern React frontend with Material-UI
✅ RESTful API backend with Python FastAPI
✅ Complete database metadata extraction
✅ Professional, responsive UI
✅ Error handling and loading states
✅ Modular and maintainable code structure
✅ Type hints and async support with FastAPI

Start by setting up the backend, creating a sample database, then build the frontend components step by step. Happy coding!
