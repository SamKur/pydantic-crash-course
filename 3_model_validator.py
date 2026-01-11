from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Any

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    # contact_details: Mapping[Literal["phone", "emergency"], str]  # to set the keys as required

    @model_validator(mode='after')  # instance methods (self) for 'after' mode, no need of @classmethod
    def validate_emergency_contact(self):
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return self

    @model_validator(mode='before')  # @classmethod required for 'before'/'wrap'
    @classmethod
    def validate_raw_input(cls, data: Any) -> Dict[str, Any]:   # data here is full input dictionary
        if isinstance(data, dict):
            # Convert age string to int early
            if 'age' in data and isinstance(data['age'], str):
                data['age'] = int(data['age'])  # Handles your '65'
            
            # Ensure contact_details has required keys for seniors
            contact = data.get('contact_details', {})
            if isinstance(contact, dict) and data.get('age', 0) > 60 and 'emergency' not in contact:
                raise ValueError("Raw input: Patients age >60 must have 'emergency' in contact_details")
            
            # Normalize allergies if single string
            allergies = data.get('allergies')
            if isinstance(allergies, str):
                data['allergies'] = [allergies]
        return data

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '65', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency':'235236'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)
