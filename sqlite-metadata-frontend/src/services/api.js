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
