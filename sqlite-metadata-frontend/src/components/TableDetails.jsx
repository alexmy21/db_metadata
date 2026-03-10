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
