from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
import shutil
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.image_services import create_image, get_image, get_images, update_image
from typing import List
from app.schemas.image import  ImageUpdate, ImageCreate
from app.models.image import Image

router = APIRouter()

# Create image directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/images", response_model = List[Image])
async def list_images(skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    images = get_images(db, skip = skip, limit = limit)
    if images is None:
        raise HTTPException(status_code=404, detail='Sorry! There are no images')
    return images

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    image_data = ImageCreate(filename=file.filename, file_path=str(file_path))
    db_image = create_image(db, image_data)
    return db_image

@router.get("./images/{image_id}")
async def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = get_image(db,image_id )
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.put("./images/{image_id}", response_model = Image)
async def update_image(image_id: int, image: ImageUpdate,  db: Session = Depends (get_db)):
    db_image = update_image(db, image_id, image )
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.delete("./images/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = delete_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail='Image not found')
        
    