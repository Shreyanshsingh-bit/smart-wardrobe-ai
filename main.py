from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from rembg import remove 

app = FastAPI()

# Helper function: Resizes standard images
def prep_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return img.resize((512, 512))

# NEW Helper function: Generates the black & white silhouette
def create_mask(image_bytes):
    # Opens the original image
    img = Image.open(io.BytesIO(image_bytes))
    
    # Use AI to remove the background (leaves it transparent)
    no_bg = remove(img)
    
    #Extracts the Alpha (transparency) channel 
    # (This creates our perfect black & white mask!)
    mask = no_bg.getchannel('A').convert("L")
    
    #Resize to match the neural network requirement
    return mask.resize((512, 512))

@app.post("/process-tryon")
async def process_tryon(user_image: UploadFile = File(...), garment_image: UploadFile = File(...)):
    print("-> Received images from Go bridge...")
    
    try:
        user_bytes = await user_image.read()
        garment_bytes = await garment_image.read()
        
        # Process the basic images
        final_user = prep_image(user_bytes)
        final_garment = prep_image(garment_bytes)
        
        # Trigger the new AI masking logic!
        print("🪄 Generating AI clothing mask...")
        garment_mask = create_mask(garment_bytes)
        
        # Save them locally temporarily so we can visually prove it worked!
        final_user.save("debug_user.jpg")
        final_garment.save("debug_garment.jpg")
        garment_mask.save("debug_mask.jpg") 
        
        print("📐 Success: Images and Mask generated!")
        
        return JSONResponse(content={
            "status": "success",
            "message": "Images successfully validated, parsed, and masked for the AI pipeline.",
            "user_dimensions": final_user.size,
            "garment_dimensions": final_garment.size,
            "mask_dimensions": garment_mask.size # <-- New success metric
        })
        
    except Exception as e:
        print(f"❌ Error processing images: {e}")
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")