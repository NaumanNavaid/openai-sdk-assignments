from pydantic import BaseModel
from typing import Optional

class MathOutPut(BaseModel):
    is_math: bool
    is_answer_69: bool
    reason: str
    
    
    
class NegativeSentimentOutput(BaseModel):
    is_negative: bool
    reason: str
    sanitized_text: str