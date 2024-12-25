from fastapi import FastAPI
from src.v1 import APIV1
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
api_v1 = APIV1()

app.mount("/assets", StaticFiles(directory="assets"), name="public")
app.include_router(api_v1.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app)