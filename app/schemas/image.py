from pydantic import BaseModel, Field, field_validator
import re

class ImageBase(BaseModel):
    filename: str
    file_path: str

class Image(ImageBase):
    id: int

class ImageUpdate(ImageBase):
    filename: str | None = None
    file_path: str | None = None
    
    
class ImageCreate(ImageBase):
    filename: str = Field(..., min_length=1, max_length=255)
    file_path: str = Field(..., min_length=1, max_length=255)    
    
    @field_validator('filename')
    def validate_filenames(cls, v):
        if not re.match(r'^[\w\-. ]+$', v):
            raise ValueError('Invalid filename')
        return v
    
    
    
class config:
    orm_mode = True

