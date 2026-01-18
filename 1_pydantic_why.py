def insert_patient_data1(name, age):
    print(name)
    print(age)
    print('inserted into db')


insert_patient_data1('susamay', 20)         # Correct data pass
insert_patient_data1('susamay', 'twenty')   # Incorrect data pass due to dynamic typing

print("=== NOW USING BUIT-IN PYTHON TYPE HINTING ===")

def insert_patient_data2(name: str, age: int) -> None :
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

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

# Step1: Pydantic Model
class Patient(BaseModel):
    name: str
    age: int    # Flexible => age: Union[str, int] OR age: str|int|None
    weight: float
    married: bool = False                   # default value
    allergies: Optional[List[str]] = None   # or [False,36.0 ,None,'Dust'] is also working because default not validated in v1! use below
    # allergies: Optional[List[str]] = Field(default=[False, 36.0, None, "Dust"] ,validate_default=True)
    # allergies: Optional[List[str]] = Field(default_factory=list)  # use this not default=[], to avoid mutable default value passed, so can infect other instances
    contact_details: Dict[str, str]

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    # print(patient.allergies)                # Let's say we're not using everything for now
    print(patient.weight)
    # print(patient.married)
    print('updated')

patient_info = {                            # Define input data (as a plain dictionary)
    'name': 'Susamay',
    'age': 26,
    'weight': 57,    # auto-converted (coerces) to 57.0
    'married': False,
    # 'allergies': ['pollen', 'dust'],
    'contact_details': {'phone': '2353462'}
}

patient1 = Patient(**patient_info)          # Step 2: Validate and parse the data (create a model instance) else ValidationError
update_patient_data(patient1)               # Step 3: Pass the validated model instance to the function

print('accessing value of phone directly - ', patient1.contact_details['phone'])

print('*'*60)
print("=== PYDANTIC v2 STYLE TYPE AND DATA VALIDATION, ADDED LATEST PRACTICES ===")

from typing import Annotated, Optional, List, Dict, Any  # py3.9+ doesnt require import except Annotated Any; use buit-in | (union), list, dict directly like Optional[bool] is same as bool | None
from pydantic import BaseModel, Field, EmailStr, AnyUrl

# Reusable type defining (Notice the '=' sign), can be re-used multiple time across classes
type NormalizedEmail = Annotated[EmailStr, Field(description="Primary contact")]    # py3.12+ the type keyword is the "modern" but is not necessity

# Step1: Pydantic Model
class Patient(BaseModel):
    # name: str = Field(max_length=50) OR simple name: str  # pydantic v1 style still can be used
    # OR below Annotated - recommended for pydantic v2 clearly separates the type from the constraints and works better with tools like: FastAPI, mypy 
    # Annotated [ data_type, Field(default, constraints, *metadatas like title, description, examples)]
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])]
    email: NormalizedEmail  # Using the alias (Notice the ':' sign)
    linkedin_url: AnyUrl
    age: int = Field(gt=0, le=120)  # DATA VALIDATION - age must be between 0 and 120
    weight: Annotated[float, Field(gt=0, strict=True)]  # strict=True means it should be exactly float, coerce to float is not allowed
    married: Annotated[Optional[bool], Field(default=None, description='Is the patient married or not')] = False    # Avoid Confusing: Two defaults but here False wins
    # OR married: Annotated[bool | None, Field(description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)] # max_items=5)] depricated
    contact_details: dict[str, str]     # Dict[str, str] earlier
    
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
