from fastapi import FastAPI,Path,HTTPException,Query
import json
app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)

@app.get("/")
def home():
    return {"message": "Welcome to the Patient Management System"}

@app.get("/view")
def view_patients():
    data = load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to view", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found") 

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="The field to sort by", example="name"),order: str = Query("asc", description="The order of sorting (asc or desc)", example="asc")):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid orders are: asc, desc")
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == "desc"))
    return sorted_data