# SQLite Metadata Frontend

A professional React application for viewing SQLite database metadata with a modern Material-UI interface.

## Features

- 📊 Database overview with statistics
- 📋 Table list with column counts
- 🔍 Detailed table schema viewer
- 🔑 Index and foreign key information
- 🎨 Professional Material-UI design
- ⚡ Fast and responsive interface

## Installation

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Setup

1. Navigate to the frontend directory:
```bash
cd sqlite-metadata-frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

### Production Build

```bash
npm run build
npm run preview
```

## Project Structure

```
sqlite-metadata-frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx           # Application header
│   │   ├── DatabaseOverview.jsx # Database stats overview
│   │   ├── TableList.jsx        # List of tables
│   │   └── TableDetails.jsx     # Table schema details
│   ├── hooks/
│   │   └── useMetadata.js       # Custom hook for API calls
│   ├── services/
│   │   └── api.js               # API service configuration
│   ├── App.jsx                  # Main application component
│   ├── main.jsx                 # Application entry point
│   └── index.css                # Global styles
├── index.html
├── package.json
└── vite.config.js
```

## Configuration

### API Endpoint

The frontend connects to the backend API. By default, it uses:
```
http://localhost:5000/api
```

To change this, edit `src/services/api.js`:
```javascript
const API_BASE_URL = 'http://your-backend-url/api';
```

## Usage

1. **Start the Backend**: Ensure the backend server is running on port 5000
2. **Start the Frontend**: Run `npm run dev`
3. **View Database**: Open `http://localhost:5173` in your browser
4. **Explore Tables**: Click on any table in the left panel to view its details
5. **View Metadata**: Use the tabs to switch between columns, indexes, and foreign keys

## Components Overview

### Header
Top navigation bar with application title and branding.

### DatabaseOverview
Displays key statistics:
- Database name
- Total number of tables
- Total number of columns

### TableList
Sidebar component showing all available tables with column counts.

### TableDetails
Main content area displaying:
- **Columns Tab**: All columns with types and constraints
- **Indexes Tab**: Database indexes
- **Foreign Keys Tab**: Relationships between tables

## Customization

### Theme

Edit the theme in `src/App.jsx`:
```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',  // Change primary color
    },
    secondary: {
      main: '#dc004e',  // Change secondary color
    },
  },
});
```

### Styling

- Global styles: `src/index.css`
- Component-level styles: Material-UI's `sx` prop
- Theme customization: `createTheme()` in App.jsx

## Troubleshooting

**API Connection Failed:**
- Verify the backend is running on port 5000
- Check the API_BASE_URL in `src/services/api.js`
- Ensure CORS is properly configured in the backend

**Dependencies Installation Issues:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Try using `npm install --legacy-peer-deps`

**Build Errors:**
- Clear cache: `npm cache clean --force`
- Update Node.js to the latest LTS version
- Check for conflicting global packages

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Material-UI (MUI)** - Component library
- **Axios** - HTTP client
- **React Router** - Navigation (installed for future use)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Tips

- Tables with many columns render quickly due to virtualization
- API calls are cached in component state
- Use React DevTools to profile component renders

## Future Enhancements

- [ ] Search and filter tables
- [ ] Export schema as JSON/SQL
- [ ] Dark mode toggle
- [ ] Table data preview
- [ ] ER diagram visualization
- [ ] Query builder interface

## License

MIT
