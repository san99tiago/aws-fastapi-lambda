# Built-in imports
import os
from typing import Union

# External imports
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel


app = FastAPI(
    description="Simple FastAPI server that runs on top of Lambda Functions.",
    contact={"Santiago Garcia Arango": "san99tiago@gmail.com"},
    title="Simple FastAPI Example",
    version="0.0.1",
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def root():
    return {"message": "Hello by Santi"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# This is the Lambda Function's entrypoint (handler)
handler = Mangum(app)
