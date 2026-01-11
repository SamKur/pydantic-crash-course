from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = "Male"
    age: int
    address: Address
    isMarried: bool = None

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

# print(patient1)      # name='nitish' gender='Male' age=35 address=Address(city='gurgaon', state='haryana', pin='122001')

temp1 = patient1.model_dump()  # serialize the model-object to a dictionary 
temp2 = patient1.model_dump_json()  # serialize the model-object to a json for api etc
print(temp2)

temp = patient1.model_dump(include=['name', 'age'], exclude= {'address':['state']} , exclude_unset=True)  # exclude attributes that are not set while creating the model-object
print(temp)
print(type(temp))


# Benefits of Nested Models
# --------------------------------

# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed

# Serialization: Nested models can be serialized easily, making it easier to convert to JSON or other formats

# Performance: Nested models can be more efficient than flat models with many fields
