from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import List,Dict,Annotated,Optional,Literal
import json
import pandas as pd
import pickle

with open('model.pkl','rb') as f:
    model=pickle.load(f)

app=FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=120,description="age of the person")]
    weight:Annotated[float,Field(...,gt=0,description="weight of the person in kg")]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description="height of the person in m")]
    income_lpa:Annotated[float,Field(...,gt=0,description="income of the person in lakhs per annum")]
    smoker:Annotated[Literal['yes','no'],Field(...,description="whether the person is a smoker or not")]   
    city:Annotated[str,Field(...,description="city of residence of the person")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="occupation of the person")]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi_value=self.weight/(self.height**2)
        return round(bmi_value,2)
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker=='yes' and self.bmi>30:
            return "high"
        elif self.smoker=='yes' or self.bmi>27:
            return "medium"
        else:
            return "low"
    @computed_field
    @property
    def age_group(self)->str:
        if self.age<25:
            return "young"
        elif 25<=self.age<45:
            return "adult"
        elif 45<=self.age<60:
            return "middle-aged"
        else:
            return "senior"
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    
@app.post("/predict")
def predict_premium(data:UserInput):
        
    input_df = pd.DataFrame([{
    'bmi': data.bmi,
    'age_group': data.age_group,
    'lifestyle_risk': data.lifestyle_risk,
    'city_tier': data.city_tier,
    'income_lpa': data.income_lpa,
    'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    class_labels = model.classes_
    
    class_probabilities = {str(label): float(prob) for label, prob in zip(class_labels, probabilities)}
    confidence = float(max(probabilities))

    return JSONResponse(status_code=200, content={
        'response': {
            'predicted_category': prediction,
            'confidence': confidence,
            'class_probabilities': class_probabilities
        }
    })