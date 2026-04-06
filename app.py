from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from utils import split_text, enhance_prompt, generate_image

# Create folders if not exist 
os.makedirs("static/images", exist_ok=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"storyboard": [], "style": "cinematic realism"}
    )


# Generate storyboard
@app.post("/", response_class=HTMLResponse)
def generate(
    request: Request,
    text: str = Form(...),
    style: str = Form("cinematic realism")
):
    sentences = split_text(text)
    storyboard = []

    for i, sentence in enumerate(sentences):
        print(f"[{i+1}/{len(sentences)}] Refining prompt...")
        prompt = enhance_prompt(sentence, style)

        print(f"[{i+1}/{len(sentences)}] Generating image...")
        image = generate_image(prompt)

        storyboard.append({
            "text": sentence,
            "prompt": prompt,
            "image": image,
        })

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"storyboard": storyboard, "original_text": text, "style": style}
    )