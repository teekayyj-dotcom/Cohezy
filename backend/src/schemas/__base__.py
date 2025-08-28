from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True # kich hoat mapping tu sqlalchemy -> pydantic
        orm_mode = True

