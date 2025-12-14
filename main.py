from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,  Literal, Optional
from fastapi.responses import JSONResponse
import json

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The ID of the patient")]
    name: Annotated[str, Field(..., description="The name of the patient")]
    city: Annotated[str, Field(..., description="The city of the patient")]
    age: Annotated[int, Field(...,gt=0, lt=120,description="The age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient")]

    # bmi & verdict will be calculated based on the height and weight
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return round(bmi,2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi >= 18.5 and self.bmi < 25:
            return "Normal"
        else: 
            return "Obese"

# Creating a new class for updating the patient data, all the fields are optional and will be updated if provided by the user
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(description="The name of the patient", default=None)]
    city: Annotated[Optional[str], Field(description="The city of the patient", default=None)]
    age: Annotated[Optional[int], Field(gt=0, lt=120, description="The age of the patient", default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(description="The gender of the patient", default=None)]
    height: Annotated[Optional[float], Field(gt=0, description="The height of the patient", default=None)]
    weight: Annotated[Optional[float], Field(gt=0, description="The weight of the patient", default=None)]

def load_data():
    with open("patients.json", 'r') as file:
        data = json.load(file)
        return data

def save_data(data):
    with open("patients.json", 'w') as file:
        json.dump(data, file)  # Appends the data to the file, overwrites the existing data

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patients records"}

@app.get("/view")
def view():
    data = load_data()
    return {"patients": data}

@app.get("/patients/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example="P001")):
    data = load_data()

    if patient_id in data:
        return {"patient": data[patient_id]}
    else:
        raise HTTPException(status_code=404, detail="Patient ID not found")


@app.get("/sort")
def sort(sort_by: str = Query(..., description="Sort on the basis of height, weight, bmi"), order: str = Query('asc', description="Sort order: asc or desc")):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field choose from {valid_fields}")

    order_fields = ["asc", "desc"]

    if order not in order_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort order choose from {order_fields}")

    data = load_data()

    sort_order = True if order=="desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data


@app.post("/create")
def create(patient: Patient):  #This is an pydantic object, the data will be sent and validated automatically
    # Load the existing data
    data = load_data()

    # Check if the patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient Already exists")

    # Add the new patient to the data
    data[patient.id] = patient.model_dump(exclude=["id"]) #exclude the id field from the model_dump, Automatically converted from pydantic object to a dictionary
    save_data(data)

    return JSONResponse(status_code=201, content={'message': "Patient created successfully"})


@app.put("/edit/{patient_id}")
def update(patient_id: str, patient_update: UpdatePatient):

    # Load the existing data
    data = load_data()

    # Check if the patient ID does not exist
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID does not exist")

    # Update the patient data
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # dict -> pydantic object -> updated BMI & verdict will be calculated automatically
    # We have to add id first
    existing_patient_info['id'] = patient_id
    patient_object = Patient(**existing_patient_info)  # Done to calculate the value of BMI & Verdict automatically
    # pydantic Object -> Dictionary 
    existing_patient_info = patient_object.model_dump(exclude=["id"])

    # Add the updated patient to the data
    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient Info. Updated Successfully"})


@app.delete("/delete/{patient_id}")
def delete(patient_id: str):
    # Load the existing data
    data = load_data()

    # Check if the patient ID does not exist
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID does not exist")

    # Delete the patient from the data
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient Info. Deleted Successfully"})