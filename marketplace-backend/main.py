from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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