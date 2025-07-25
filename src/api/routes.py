from src.utils.logger import logger
from src.backend.code_iterator import CodeIteratorOrchestrator
from src.api.models import CodeRequest, CodeResponse, HealthResponse
from fastapi import APIRouter, HTTPException


# Create the router instance
router=APIRouter()

# Initialize the orchestrator
orchestrator=CodeIteratorOrchestrator()

# Define the health check endpoint
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """ Health check endpoint."""
    logger.info("Health check requested")
    return HealthResponse(
        status="Healthy",
        message="Code iterator API is running"
    )


# Define the code iterator endpoint
@router.post("/suggest-code", response_model=CodeResponse)
async def suggest_code(request: CodeRequest):
    """ Main endpoint for code improvement suggestions"""
    try: 
        logger.info("Code suggestion requested")

        # Basic input validation
        if not request.original_code.strip():
            raise HTTPException( status_code=400, detail="Original code cannot be empty")
        
        if not request.user_prompt.strip():
            raise HTTPException( status_code=400, detail="User prompt cannot be empty")

        # Process the request through the orchestrator
        result= orchestrator.process_code_request(original_code=request.original_code, user_prompt=request.user_prompt)

        # Return the response
        return result

    except Exception as e:
        logger.error(f"Unexpected error:{str(e)}")
        raise HTTPException(status_code= 500, detail=f"Internal server error: {str(e)}")
        

        


