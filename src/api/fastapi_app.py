from src.api.routes import router
from fastapi import FastAPI

# Create the FastAPI app instance
app= FastAPI(
    title="Code Iterator AI API",
    description= "AI-powered code improvement tool",
    docs_url="/docs"
)

# Include the router
app.include_router(router, prefix='/api')