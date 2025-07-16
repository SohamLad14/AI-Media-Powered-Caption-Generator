from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import logging
from datetime import datetime

from vision import ImageClassifier
from caption import ImageCaptioner
from enhancer import CaptionEnhancer

UPLOAD_FOLDER = "temp_uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI(title="AI Image Caption Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    classifier = ImageClassifier()
    captioner = ImageCaptioner()
    enhancer = CaptionEnhancer()
    logger.info("Models loaded successfully.")
except Exception as e:
    logger.error(f"Model loading failed: {e}")
    classifier = captioner = enhancer = None

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if all([classifier, captioner, enhancer]) else "degraded",
        "models": {
            'classifier': classifier is not None,
            'captioner': captioner is not None,
            'enhancer': enhancer is not None
        },
        "timestamp": str(datetime.now())
    }

@app.post("/generate")
async def generate_caption_and_labels(
    image: UploadFile = File(...),
    length: int = Form(50)  # optional: change default if needed
):
    if not all([classifier, captioner, enhancer]):
        return JSONResponse(status_code=500, content={"error": "Models not properly loaded"})

    image_path = None

    try:
        filename = image.filename
        if not allowed_file(filename):
            return JSONResponse(status_code=400, content={"error": "Invalid file type"})

        contents = await image.read()
        if len(contents) > MAX_FILE_SIZE:
            return JSONResponse(status_code=400, content={"error": "File too large"})

        image_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(image_path, 'wb') as f:
            f.write(contents)

        logger.info("Classifying image...")
        classification_result = classifier.classify_image(image_path, top_k=5)

        logger.info("Generating base caption...")
        caption_result = captioner.generate_caption(image_path, max_length=length)

        logger.info("Enhancing caption...")
        enhanced_result = enhancer.enhance_caption(
            caption_result,
            classification_result
        )

        logger.info(f"Enhanced Caption: {enhanced_result.get('enhanced_caption')}")

        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        return {
            "base_caption": caption_result.get("caption", ""),
            "labels": [label["label"] for label in classification_result],
            "enhanced_caption": enhanced_result.get("enhanced_caption", "Enhancement failed.")
        }

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        return JSONResponse(status_code=500, content={"error": str(e)})
