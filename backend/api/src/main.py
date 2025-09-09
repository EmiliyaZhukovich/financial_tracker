from fastapi import FastAPI
import uvicorn
from models.get_db import init_db

app = FastAPI()

init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5050, reload=True)
