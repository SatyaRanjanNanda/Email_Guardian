import logging
from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from backend_model import predict, retrain, LABELS

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("email_guardian.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000", # Alternate localhost
        "http://localhost:3001", # React dev server (actual port)
        "http://127.0.0.1:3001", # Alternate localhost (actual port)
        "http://localhost:55060", # Production static server
        # Add your production domain below:
        # "https://your-production-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    text: Optional[str] = None

class RetrainRequest(BaseModel):
    texts: List[str]
    labels: List[str]

@app.post('/classify')
def classify_email(request: EmailRequest):
    logger.info(f"/classify request: {request.text}")
    if not request.text:
        logger.warning("No email text provided.")
        return {"error": "No email text provided."}
    try:
        label = predict(request.text)[0]
        logger.info(f"Predicted label: {label}")
        return {"label": label}
    except Exception as e:
        logger.error(f"Error in /classify: {e}", exc_info=True)
        return {"error": "Internal server error. Please try again later."}

@app.post('/classify_file')
def classify_email_file(file: UploadFile = File(...)):
    try:
        content = file.file.read().decode('utf-8')
        logger.info(f"/classify_file request: {file.filename}")
        label = predict(content)[0]
        logger.info(f"Predicted label: {label}")
        return {"label": label}
    except Exception as e:
        logger.error(f"Error in /classify_file: {e}", exc_info=True)
        return {"error": "Internal server error. Please try again later."}

@app.post('/retrain')
def retrain_model(request: RetrainRequest):
    logger.info(f"/retrain request: {len(request.texts)} samples")
    if len(request.texts) != len(request.labels):
        logger.warning("Texts and labels must be the same length.")
        return {"error": "Texts and labels must be the same length."}
    if not all(label in LABELS for label in request.labels):
        logger.warning(f"Invalid label in request: {request.labels}")
        return {"error": f"Labels must be one of {LABELS}"}
    try:
        retrain(request.texts, request.labels)
        logger.info("Model retrained successfully.")
        return {"message": "Model retrained successfully."}
    except Exception as e:
        logger.error(f"Error in /retrain: {e}", exc_info=True)
        return {"error": "Internal server error. Please try again later."}

@app.options("/classify")
def options_classify():
    return Response(status_code=200) 