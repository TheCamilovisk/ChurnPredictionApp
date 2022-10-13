from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from churn_api.routers import predict, features

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
)

app.include_router(predict.router)
app.include_router(features.router)


@app.get("/")
async def root():
    return {"message": "Churn prediction API"}
