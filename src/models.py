from pydantic import BaseModel


# Input structure of user's message
class ChatRequest(BaseModel):
    message: str


# Output structure of AI response
class ChatResponse(BaseModel):
    response: str