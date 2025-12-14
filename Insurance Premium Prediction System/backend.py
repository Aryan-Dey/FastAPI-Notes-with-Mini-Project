from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal, Optional
from Model.predict import predict_output, model
from Schema.input_val import UserInput
from Schema.response_val import PredictionResponse

app = FastAPI()

# Home Endpoint - Human Readable Output (needed for Swagger UI, etc.)
@app.get("/")
def home():
    return JSONResponse(status_code=200, content={'message': "Welcome to the Insurance Premium Prediction API"})

# Health Check Endpoint - Machine Readable Output (needed for AWS, Kubernetes, etc.)
@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "model_status": "Loaded" if model is not None else "Not Loaded",
        "Version": "1.0.0"
    }

@app.post("/predict", response_model = PredictionResponse)
def predict_premium(data: UserInput):

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    input_df = {
        "age": data.age,
        "income_lpa": data.income_lpa,
        "BMI": data.bmi,
        "smoker": data.smoker,
        "occupation": data.occupation,
        "Age Group": data.age_group,
        "City Tier": data.city_tier,
        "Lifestyle Risk": data.lifestyle_risk
    }

    try:
        prediction = predict_output(input_df)
        return JSONResponse(status_code=200, content={'response': prediction})

    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})
