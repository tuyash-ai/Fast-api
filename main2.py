from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import List,Dict,Annotated,Optional,Literal
import json

from main import load_data
app=FastAPI()

class Patient(BaseModel):

    id:Annotated[str,Field(...,description="patient id",example="P001")]
    name:Annotated[str,Field(...,max_length=50,description="patient name")]
    city:Annotated[str,Field(...,description="patient city")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="patient age")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="gender of patient")]
    height:Annotated[float,Field(...,gt=0,description="height of patient in cm")]
    weight:Annotated[float,Field(...,gt=0,description="weight of patient in kg")]

    @computed_field
    @property
    def bmi(self)->float:
        height_in_meters=self.height/100
        bmi_value=self.weight/(height_in_meters**2)
        return round(bmi_value,2)
    @computed_field
    @property
    def category(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_patients():
    with open("patients.json", "r") as f:
        data=json.load(f)
    return data

def save_patient(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)

@app.get("/")
def home():
    return {"message": "Welcome to the Patient Management System"}

@app.get("/view")
def view_patients():
    data = load_patients()
    return data

@app.post("/create")
def create_patient(patient: Patient): #validation and type coercion happens here
    data=load_patients()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    data[patient.id]=patient.model_dump(exclude=["id"])

    save_patient(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})