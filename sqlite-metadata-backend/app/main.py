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
