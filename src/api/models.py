from pydantic import BaseModel, Field
from typing import Dict

# Define the Request Schema
class CodeRequest(BaseModel):

    """ Request model for code improvement."""

    original_code: str= Field(..., description="The original code to be improved")
    user_prompt: str= Field(..., description="User's instruction for code improvement")


# Define the Response Schema
class CodeResponse(BaseModel):

    """ Response model for code improvement"""

    original_code: str= Field(..., description= "The original code submitted")
    improved_code: str= Field(..., description="The AI- improved code")
    explanation: str= Field(..., description="Explanation of changes made")
    diff: Dict= Field(..., description="Diff information between original and improved code")
    success: bool= Field(..., description=" Whether the operation was successful or not.")


# Health check Schema
class HealthResponse(BaseModel):
    
    """ Health check response"""

    status: str= Field(..., description="API Status")
    message: str = Field(..., description="Health check message")