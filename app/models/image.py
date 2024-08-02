from sqlalchemy import Column, Integer, String
from app.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, index=True)
    year = Column(Integer, index=True)
    event = Column(String, index=True)