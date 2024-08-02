from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas.image import ImageUpdate, ImageCreate

def create_image(db: Session, image_data: ImageCreate):
    db_image = models.Image(filename = image_data.filename,file_path = image_data.file_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def get_images(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Image).offset(skip).limit(limit).all()

def update_image(db: Session, image_id: int, image: ImageUpdate):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if db_image:
        update_data = image.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_image, key, value)
        db.commit()
        db.refersh(db_image)
    return db_image

def delete_image(db: Session, image_id: int):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
        return True
    return False
