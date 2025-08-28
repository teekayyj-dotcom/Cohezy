from typing import Optional
from pydantic import Field
from .__base__ import BaseSchema

class ManageResponse(BaseSchema):
    message: str = Field(..., description="A message indicating the result of the operation")
    detail: Optional[str] = Field(None, description="Additional details about the operation")

class ErrorResponse(BaseSchema):
    error: str = Field(..., description="A brief error message")
    detail: Optional[str] = Field(None, description="Detailed information about the error")

class Pagination(BaseSchema):
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")

