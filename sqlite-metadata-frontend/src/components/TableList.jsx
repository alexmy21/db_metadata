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
