import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import HTTPException

class MetadataController:
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(__file__), 
                                       '../../database/sqlite_test')
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
