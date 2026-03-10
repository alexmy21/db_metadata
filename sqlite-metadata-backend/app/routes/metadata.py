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
