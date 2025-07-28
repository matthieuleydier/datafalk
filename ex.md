# Context

You are joining Photofalk, a startup focused on AI-powered enhancement of advertising images.  
The team builds visual automation tools for agencies and brands, integrated into a production platform.

Your task: deliver a standalone microservice capable of removing the background from an image.  
This service will be integrated into our product later, but for now must work as a complete local demo.

# Objective

Develop a Python service that:

- exposes an HTTP API
- uses a Redis-backed job queue for processing
- provides a web demo interface for image upload and result visualization
- is fully containerized, with a provided `docker-compose.yml`

# Specifications

## REST API

- `POST /remove-bg`: upload an image, returns a `job_id`
- `GET /status/{job_id}`: returns job status (`queued`, `processing`, `done`, `failed`)
- `GET /result/{job_id}`: returns the processed image (404 if not ready)

## Job Queue

- Uses a Redis queue with a worker (Celery, RQ, Arq, etc.)
- Processing is asynchronous

## Image Processing

- Uses an existing library (`rembg`)
- The returned image must have the background removed (PNG format recommended)

## Demo Interface

- Displays an image upload form
- Shows both the original and processed image when ready
- Can poll `/status` or use SSE (see bonus)

## docker-compose.yml

- launches the API
- launches the worker
- launches Redis

Each component should have its own Dockerfile if needed.

## Bonus

- `GET /events/{job_id}`: SSE (Server-Sent Events) for progress updates
- Automatic cleanup of files after X minutes
- Durable queue in case of crash (persistent Redis)
- Automated tests (unit or HTTP)

### Enhanced Demo UI Ideas

- Add drag-and-drop support for image upload, with instant preview before submission.
- Show a real-time progress bar or spinner while waiting for background removal.
- Display error messages clearly if processing fails or the image is invalid.
- Allow users to download the processed PNG directly from the interface.
- Optionally, let users compare before/after images side-by-side or with a slider.
- Show job queue position or estimated wait time if possible.
- Support mobile-friendly/responsive design for the demo page.