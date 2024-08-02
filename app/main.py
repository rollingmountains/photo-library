from fastapi import FastAPI, Request
from app.database import engine
from app.models import image
from app.routers.image import router as image_router
from fastapi.responses import JSONResponse


app = FastAPI()

app.include_router(image_router, prefix="/api/v1")
# Create database tables
image.Base.metadata.create_all(bind=engine)




@app.get("/")
async def root():
    return "Hello Photo Gallery"

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"},
    )

