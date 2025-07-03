from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

app = FastAPI()

# Конфигурация путей
MODEL_NAME = "utrobinmv/t5_translate_en_ru_zh_large_1024_v2"
LOCAL_TOKENIZER_PATH = "./models/t5_tokenizer"  # Папка с spiece.model

# Загрузка токенизатора из локального файла
tokenizer = T5Tokenizer.from_pretrained(LOCAL_TOKENIZER_PATH)

# Загрузка модели ТОЛЬКО из облака (веса не сохраняются локально)
model = T5ForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    local_files_only=False  # Всегда грузит модель из интернета
)

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.get("/", response_class=HTMLResponse)
async def translation_form(translated_text: str = ""):
    return f"""
    <html>
    <body>
        <h1>Переводчик</h1>
        <form action="/translate">
            <textarea name="text" style="width:80%;height:100px"></textarea>
            <button type="submit">Перевести</button>
        </form>
        {f'<div style="margin-top:20px;padding:10px;border:1px solid #ddd">{translated_text}</div>' if translated_text else ''}
    </body>
    </html>
    """

@app.get("/translate/", response_class=HTMLResponse)
async def translate_text(text: str):
    try:
        input_text = "translate to ru: " + text
        input_ids = tokenizer(input_text, return_tensors="pt").to(device)
        with torch.no_grad():
            translated_ids = model.generate(**input_ids)
        translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        return await translation_form(translated_text=translated_text)
    except Exception as e:
        return await translation_form(translated_text=f"Ошибка: {str(e)}")