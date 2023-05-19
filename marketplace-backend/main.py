from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Make sure to allow CORS for your Vue.js application
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    with open(file.filename, 'wb+') as f:
        f.write(await file.read())
    return {"filename": file.filename}

@app.get("/download/{filename}")
async def read_upload(filename: str):
    file_location = f"{filename}"
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_location)