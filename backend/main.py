# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
from pydantic import BaseModel
from typing import List

from baxiCode import Validation

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


@app.get("/")
async def root():
    print("hello world")
    return {"message": "Hello World"}


@app.post("/process_data")
async def process_data(item: Item):
    print(item)
    processed_data = item.data
    print(processed_data)
    result = Validation(processed_data)
    print(result)
    return (result)
