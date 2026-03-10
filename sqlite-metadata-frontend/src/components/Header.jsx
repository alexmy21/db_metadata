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
