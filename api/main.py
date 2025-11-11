from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io, json

app = FastAPI()

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

    # Xử lý metadata (convert các giá trị bytes -> str)
    safe_info = {}
    for k, v in image.info.items():
        try:
            if isinstance(v, bytes):
                safe_info[k] = v.decode("utf-8", errors="ignore")
            else:
                # đảm bảo giá trị có thể JSON serialize
                json.dumps(v)
                safe_info[k] = v
        except Exception:
            safe_info[k] = str(v)

    return {
        "filename": file.filename,
        "format": format,
        "mode": mode,
        "width": width,
        "height": height,
        "metadata": safe_info,
    }
