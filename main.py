from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageOps
import io

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_to_grf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        
        # Inversão de cores para bater com seu exemplo (fundo 0000)
        img = img.convert('L')
        img = ImageOps.invert(img)
        img = img.convert('1')
        
        width, height = img.size
        bytes_per_row = (width + 7) // 8
        total_bytes = bytes_per_row * height
        
        image_bytes = img.tobytes()
        hex_data = image_bytes.hex().upper()
        
        hex_formatted = ""
        for i in range(0, len(hex_data), 64):
            hex_formatted += hex_data[i:i+64] + "\n"
        
        # Pegamo o nome do arquivo enviado 
        nome_arquivo_limpo = file.filename.split('.')[0].upper()
        cabecalho = f"~DG{nome_arquivo_limpo},{total_bytes:05d},{bytes_per_row:03d},"

        conteudo_final = cabecalho + "\n" + hex_formatted
        
        file_output = io.BytesIO(conteudo_final.encode('utf-8'))
        nome_download = f"{nome_arquivo_limpo}.grf"
        
        return StreamingResponse(
            file_output,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={nome_download}"}
        )
    
    except Exception as e:
        return {"error": f"Erro ao processar: {str(e)}"}