from fastapi import FastAPI
import uvicorn
from models.get_db import init_db
from revenue.rest import router as revenue_router
from expenses.rest import router as expenses_router


app = FastAPI()

app.include_router(revenue_router, tags=['revenue'])
app.include_router(expenses_router, tags=["expenses"])

init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5050, reload=True)
