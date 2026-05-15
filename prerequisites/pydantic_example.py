from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(...,max_length=50,description="The full name of the patient", example="John Doe")] # Using Annotated to add metadata for the name field
    age: int=Field(...,gt=0,lt=120) # Using Field to add validation for age, it must be greater than 0 and less than 120
    email: EmailStr # Using EmailStr from Pydantic to validate email addresses
    weight: float=Field(..., gt=0,strict=True,description="Weight of the patient in kg") # Using Field to add validation for weight, it must be greater than 0,strictly a float, and adding a description for documentation
    married: bool = False # Default value for married is False, if not provided it will be set to False
    allergies: Optional[List[str]] = None # Optional field for allergies, it can be None or a list of strings
    contact_details: Dict[str, str]
    LinkedIn: Optional[AnyUrl] = None # Optional field for LinkedIn profile URL, it can be None or a valid URL


def create_patient(patient: Patient):
    print(f"Creating patient with name: {patient.name} and age: {patient.age}")
    print(f"Contact details: {patient.contact_details}")
    if patient.allergies:
        print(f"Allergies: {', '.join(patient.allergies)}")
    else:        
         print("Allergies: None")
    print(f"Married: {'Yes' if patient.married else 'No'}")
    print(f"Weight: {patient.weight} kg")
    print("Patient created successfully!")

def update_patient(patient: Patient):
    print(f"Updating patient with name: {patient.name} and age: {patient.age}")


patient1_data = {"name": "John Doe", "age": 30, "email": "john.doe@example.com", "weight": 70., "contact_details": {"phone": "123-456-7890"}, "married": True, "allergies": ["pollen", "dust"]}
patient2_data = {"name": "Jane Smith", "age": 25, "email": "jane.smith@example.com", "weight": 60., "contact_details": {"phone": "987-654-3210"}, "married": False, "allergies": None}

patient1 = Patient(**patient1_data) #dict unpacking to create a Patient instance
patient2 = Patient(**patient2_data) #dict unpacking to create a Patient instance
create_patient(patient1)
create_patient(patient2)
