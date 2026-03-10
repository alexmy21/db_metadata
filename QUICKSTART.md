# 🚀 Quick Start Guide

Get the SQLite Metadata Viewer running in 5 minutes!

## Option 1: Automated Setup (Recommended for Windows)

Run the all-in-one setup script:

```bash
setup-all.bat
```

This will automatically set up both backend and frontend.

## Option 2: Manual Setup

### Step 1: Setup Backend

```bash
cd sqlite-metadata-backend
setup.bat
```

### Step 2: Setup Frontend

```bash
cd sqlite-metadata-frontend
setup.bat
```

## Running the Application

### Terminal 1 - Start Backend
```bash
cd sqlite-metadata-backend
start-backend.bat
```
✅ Backend running at: http://localhost:5000

### Terminal 2 - Start Frontend
```bash
cd sqlite-metadata-frontend
start-frontend.bat
```
✅ Frontend running at: http://localhost:5173

### Open Browser
Navigate to: **http://localhost:5173**

## What You'll See

1. **Database Overview** - Statistics about your database
2. **Table List** - All tables in the left sidebar
3. **Table Details** - Click any table to view:
   - Columns and their types
   - Indexes
   - Foreign key relationships

## Sample Database

The setup creates a sample database with:
- **users** table (4 columns)
- **posts** table (6 columns)
- **comments** table (5 columns)
- Sample indexes and foreign keys

## Using Your Own Database

1. Copy your `.db` file to: `sqlite-metadata-backend/database/`
2. Edit `sqlite-metadata-backend/.env`:
   ```
   DB_PATH=./database/your-database.db
   ```
3. Restart the backend server

## Troubleshooting

### "Python not found"
- Install Python 3.8+ from python.org
- Make sure it's added to PATH

### "npm not found"
- Install Node.js 16+ from nodejs.org

### "Port already in use"
Backend: Edit PORT in `sqlite-metadata-backend/.env`
Frontend: Vite will auto-select next available port

### "Cannot connect to API"
- Ensure backend is running on port 5000
- Check browser console for errors
- Verify no firewall is blocking localhost

## API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## Next Steps

✅ Explore the sample database
✅ Connect your own SQLite database
✅ Customize the UI theme in `src/App.jsx`
✅ Add new features

## Need Help?

Check the full documentation:
- [Main README](README.md)
- [Backend README](sqlite-metadata-backend/README.md)
- [Frontend README](sqlite-metadata-frontend/README.md)
- [Comprehensive Guide](sqlite-metadata-app-guide.md)

---

**Enjoy exploring your SQLite databases! 🎉**
