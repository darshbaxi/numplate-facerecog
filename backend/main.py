# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
from pydantic import BaseModel
from typing import List

from mainPic2 import Validation

app = FastAPI()

# Add CORS middleware to allow requests from your Vue.js application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with the actual origin of your Vue.js app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    data: str

@app.post("/process_data")
async def process_data(item: Item):
    processed_data = item.data

    celeb_ids = Validation(processed_data)
    print(celeb_ids)
    return {"celeb_ids": celeb_ids}
