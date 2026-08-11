from pydantic import BaseModel,ConfigDict
from datetime import datetime


# What the frontend sends us
class InterviewCreate(BaseModel):
    user_name : str
    persona : str


class InterviewResponse(BaseModel):
    session_id : str 
    user_name : str
    persona : str
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)



