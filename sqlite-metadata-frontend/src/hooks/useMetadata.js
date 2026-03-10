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
