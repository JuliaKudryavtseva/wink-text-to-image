from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
import os
from datetime import datetime

from app.models.model_loader import ImageGenerator
from app.utils.image_utils import save_image, cleanup_old_files

app = FastAPI(title="Text-to-Image Service")
templates = Jinja2Templates(directory="app/templates")

# Инициализация генератора
generator = ImageGenerator()

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_image(
    request: Request,
    prompt: str = Form(...),
    negative_prompt: str = Form(""),
    num_steps: int = Form(20),
    guidance_scale: float = Form(7.5),
    width: int = Form(512),
    height: int = Form(512)
):
    try:
        # Генерация изображения
        image = generator.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height
        )
        
        # Сохранение изображения
        filename = f"{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = save_image(image, filename)
        
        # Очистка старых файлов
        cleanup_old_files(max_files=1000)
        
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request,
                "image_url": f"/outputs/{filename}",
                "prompt": prompt,
                "filename": filename
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request,
                "error": str(e)
            }
        )

@app.get("/download/{filename}")
async def download_image(filename: str):
    file_path = os.path.join("outputs", filename)
    return FileResponse(
        file_path, 
        media_type='image/png',
        filename=f"generated_{filename}"
    )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "text-to-image"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)