from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()

# Cho phép gọi API từ web khác (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello Render!"}


# 📸 API: Nhận file ảnh, trả thông tin ảnh
@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception as e:
        return {"error": f"Không thể đọc ảnh: {str(e)}"}

    width, height = image.size
    format = image.format
    mode = image.mode
    info = image.info  # metadata (EXIF, dpi, ...)

    return {
        "filename": file.filename,
        "format": format,
        "mode": mode,
        "width": width,
        "height": height,
        "metadata": info,
    }
