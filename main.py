from fastapi import FastAPI
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