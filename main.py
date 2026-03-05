from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from zplgrf import GRF
import io

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_to_grf(file: UploadFile = File(...)):
    try:
        # 1. Lê os bytes do arquivo enviado
        contents = await file.read()
        
        # 2. Abre com Pillow para converter para preto e branco (1-bit)
        # Isso garante que formatos como PCX sejam processados corretamente
        img = Image.open(io.BytesIO(contents))
        img = img.convert('1')
        
        # 3. Em vez de passar os bytes para o GRF, salvamos a imagem 
        # processada em um buffer e passamos os bytes desse buffer
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG') # PNG é um formato seguro intermediário
        
        # 4. Agora sim passamos os bytes corretos para a biblioteca ZPL
        grf = GRF.from_image(img_byte_arr.getvalue(), "UPLOAD")
        
        return {"zpl": grf.to_zpl()}
    
    except Exception as e:
        return {"error": f"Erro ao processar: {str(e)}"}