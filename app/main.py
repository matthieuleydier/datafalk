from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from redis import Redis
from rq import Queue
import uuid
import os
from rembg import remove
from starlette.templating import Jinja2Templates
import io
from pathlib import Path

from tasks import process_image

# Redis connection and queue
redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)



@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    job_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{job_id}.png")
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.png")

    # Save uploaded file
    contents = await file.read()
    with open(input_path, "wb") as f:
        f.write(contents)

    # Enqueue background removal job
    # job = queue.enqueue(process_image, input_path, output_path, job_id=job_id)
    job = queue.enqueue("tasks.process_image", input_path, output_path, job_id=job_id)
    return {"job_id": job.get_id()}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"status": "not found"})
    return {"status": job.get_status()}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.png")
    if not os.path.isfile(output_path):
        return JSONResponse(status_code=404, content={"error": "Result not ready"})
    return StreamingResponse(open(output_path, "rb"), media_type="image/png")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
