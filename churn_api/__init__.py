from fastapi import FastAPI

import churn_api.routers.predict as predict

app = FastAPI()


app.include_router(predict.router)


@app.get("/")
async def root():
    return {"message": "Churn prediction API"}
