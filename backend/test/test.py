from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil

app = FastAPI()

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
  try:
    with open(file.filename, 'wb') as f:
      shutil.copyfileobj(file.file, f)
  except Exception:
    raise HTTPException(status_code=500, detail="Something went wrong")
  finally:
    file.file.close()
  
  return {"Message": f"successfully uploaded {file.filename}"}

import uvicorn
uvicorn.run(app, port=8000)