def insert_patient_data1(name, age):
    print(name)
    print(age)
    print('inserted into db')


insert_patient_data1('susamay', 20)         # Correct data pass
insert_patient_data1('susamay', 'twenty')   # Incorrect data pass due to dynamic typing

print("=== NOW USING BUIT-IN PYTHON TYPE HINTING ===")

def insert_patient_data2(name, age):
    print(name)
    print(age)
    print('inserted into db with type hinting')


insert_patient_data2('susamay', 'twenty')   # Type hinting does not enforce type checking at runtime

print("=== NOW USING MANUAL TYPE CHECKING ===")

def insert_patient_data3(name, age):
    if not isinstance(name, str):           # or, if type(name) is not str:
        raise TypeError('Name must be a string')
    if not isinstance(age, int):
        raise TypeError('Age must be an integer')
    if age < 0 or age > 120:                # data validation
        raise ValueError('Age must be between 0 and 120')
    print(name)
    print(age)
    print('inserted into db with manual type checking // Not Scalable')

# insert_patient_data3('susamay', 'twenty')  # Throws TypeError
insert_patient_data3('susamay', 20)          # Correct data pass -> we need to write this checks for every function


print("=== INSTEAD USE PYDANTIC FOR TYPE AND DATA VALIDATION ===")
print("=== SIMPLE USAGE OF PYDANTIC ===")

from pydantic import BaseModel
from typing import List, Dict, Optional

# Step1: Pydantic Model
class Patient(BaseModel):
    name: str # Flexible => age: Union[str, int]
    age: int
    weight: float
    married: bool = False                   # default value
    allergies: Optional[List[str]] = None   # Optional but having default value
    contact_details: Dict[str, str]

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    # print(patient.allergies)              # Let's say we're not using everything for now
    # print(patient.married)
    print('updated')

patient_info = {                            # Define input data (as a plain dictionary)
    'name': 'Susamay',
    'age': 26,
    'weight': 57.5,    
    'married': False,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'phone': '2353462'}
}

patient1 = Patient(**patient_info)          # Step 2: Validate and parse the data (create a model instance) else ValidationError
update_patient_data(patient1)               # Step 3: Pass the validated model instance to the function


print("=== PYDANTIC v2 STYLE TYPE AND DATA VALIDATION ===")


from typing import Annotated, Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr, AnyUrl

# Step1: Pydantic Model
class Patient(BaseModel):
    # name: str = Field(max_length=50)  # pydantic v1
    # OR below Annotated - recommended for pydantic v2 clearly separates the type from the constraints and works better with tools like: FastAPI, mypy 
    # Annotated [ data_type, Field(default, constraints, *metadatas like title, description, examples)]
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)  # DATA VALIDATION - age must be between 0 and 120
    weight: Annotated[float, Field(gt=0, strict=True)]  # strict=True means it should be exactly float, coerce to float is not allowed
    married: Annotated[Optional[bool], Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_items=5)]
    contact_details: Dict[str, str]
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

# Define input data (as a plain dictionary)
patient_info = {
    'name': 'SusamAY',
    'email': 'sk@gmail.com',
    'linkedin_url': 'http://linkedin.com/in/susamay-sk',
    'age': 26,  # pass as int
    'weight': 55.2,
    'contact_details': {'phone': '4209211'}
}

# Step 2: Validate and parse the data (create a model instance) else ValidationError
patient1 = Patient(**patient_info)

# Step 3: Pass the validated model instance to the function
update_patient_data(patient1)
