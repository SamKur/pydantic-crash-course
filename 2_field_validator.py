from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, ConfigDict
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    model_config = ConfigDict(strict=None) # by default None ie safe & obvious coercion allowed
                                           # '32' str to 32 int || 32.2 float -> 32 int
    
    # name: str = "UNKNOWN UNKNOWN"          # Pydantic v1 style
    # name: Optional[str] = Field(default="UNKNOWN UNKNOWN", description="Patient name") # Pydantic v1/v2 hybrid, Field is metadata, 
                                                                                         # but ambigous for IDE/mypy, as name is treated as FieldInfo (not str)
    name: Annotated[Optional[str], Field(default="UNKNOWN UNKNOWN", description="Patient name")]  # v2-recommended, cleaner for modern usage
    
    email: EmailStr
    age: int
    weight: float = Field(gt=0, lt=150, default=50, description='A decimal value representing the weight of the patient')
    married: bool = None    # Optional
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '30', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)
