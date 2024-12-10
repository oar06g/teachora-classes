from fastapi import FastAPI
from src.v1 import APIV1

app = FastAPI()
api_v1 = APIV1()

app.include_router(api_v1.router)