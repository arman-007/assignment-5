from pydantic import BaseModel, constr, PositiveFloat

class NewDestinationModel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    description: constr(strip_whitespace=True, min_length=1)
    location: constr(strip_whitespace=True, min_length=1)
