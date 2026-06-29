from fastapi import FastAPI, File, UploadFile, HTTPException
from contextlib import asynccontextmanager
import torch
import uvicorn
from PIL import Image
import io

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Waking up the AI Engine...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware detected: Running on {device.upper()}")
    ml_models["device"] = device
    print("AI Model engine structured! Ready for requests.")
    yield
    print("Shutting down AI Engine and clearing memory...")
    ml_models.clear()

app = FastAPI(title="Smart Wardrobe AI Microservice", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "AI Microservice is online and ready"}

@app.post("/process-tryon")
async def process_tryon(
    user_image: UploadFile = File(...), 
    garment_image: UploadFile = File(...)
):
    print(f"Received images: {user_image.filename} & {garment_image.filename}")
    
    try:
        
        user_bytes = await user_image.read()
        garment_bytes = await garment_image.read()

        user_pil = Image.open(io.BytesIO(user_bytes)).convert("RGB")
        garment_pil = Image.open(io.BytesIO(garment_bytes)).convert("RGB")

        target_size = (512, 512)
        resized_user = user_pil.resize(target_size, Image.Resampling.LANCZOS)
        resized_garment = garment_pil.resize(target_size, Image.Resampling.LANCZOS)
        
        print(f"Success: Both images resized to {target_size}")
        return {
            "status": "success",
            "message": "Images successfully validated, parsed, and sized for the AI pipeline.",
            "user_dimensions": resized_user.size,
            "garment_dimensions": resized_garment.size
        }
        
    except Exception as e:
        print(f"Pipeline Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to process images: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)