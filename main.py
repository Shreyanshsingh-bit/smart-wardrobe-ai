from fastapi import FastAPI, File, UploadFile
import uvicorn
app = FastAPI(title="Smart Wardrobe AI Microservice") # initializing the API engine
# a simple check
@app.get("/")
async def root():
    return {"status": "AI Microservice is online and ready"}

#The Try-On Endpoint (Accepts images)
@app.post("/process-tryon")
async def process_tryon(
    user_image: UploadFile = File(...), 
    garment_image: UploadFile = File(...)
):
    # Log what the server received
    print(f"-> Received User Image: {user_image.filename}")
    print(f"-> Received Garment Image: {garment_image.filename}")
    

    return {
        "message": "Images received successfully. AI processing pending.",
        "user_file": user_image.filename,
        "garment_file": garment_image.filename
    }

if __name__ == "__main__":
    # Start the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)