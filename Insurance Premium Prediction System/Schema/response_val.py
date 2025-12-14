from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="Predicted Insurance Premium Category", example="Low")
    confidence: float = Field(..., description="Confidence of the prediction", example=0.8)
    class_probabilities: Dict[str, float] = Field(..., description="Probabilities for each category", example={"Low": 0.6, "Medium": 0.3, "High": 0.1})