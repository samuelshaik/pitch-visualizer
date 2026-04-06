# 🎬 Pitch Visualizer — AI Storyboard Generator

Transform any narrative into a multi-panel visual storyboard using a two-stage AI pipeline: **LLM prompt engineering → Stable Diffusion image generation**.

---

## Overview

Pitch Visualizer converts plain text into a sequence of visual scenes using a two-stage AI pipeline:

1. **Splits** the text into individual scenes using NLTK sentence tokenization
2. **Refines** each plain sentence into a rich, cinematic image prompt using Groq's Llama-3 LLM
3. **Generates** a unique AI image for each prompt via Hugging Face (Stable Diffusion XL)
4. **Presents** everything as a beautiful HTML storyboard with the original text, refined prompt, and generated image per scene

---

##  Features

-  AI-powered prompt refinement
-  Multiple visual styles (cinematic, watercolor, Pixar, etc.)
-  Automatic image generation per scene
-  FastAPI backend with clean UI
-  Fallback image generation (Pollinations)

 ---
 
## System Architecture

```
User Input (text + style)
        │
        ▼
┌─────────────────────┐
│   FastAPI (app.py)  │  ← Web server & routing
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  NLTK Tokenizer     │  ← Splits text into sentences (scenes)
│  (utils.py)         │
└────────┬────────────┘
         │  [sentence 1, sentence 2, ...]
         ▼
┌─────────────────────┐
│  Groq API           │  ← LLM prompt refinement (Llama-3.1)
│  enhance_prompt()   │    "employees frustrated" →
│                     │    "Low-angle office shot, dim light,
│                     │     frustrated faces in window reflections..."
└────────┬────────────┘
         │  [rich visual prompt]
         ▼
┌─────────────────────┐
│  Hugging Face API   │  ← Stable Diffusion XL image generation
│  generate_image()   │    Falls back to Pollinations.ai if unavailable
└────────┬────────────┘
         │  [base64 image data]
         ▼
┌─────────────────────┐
│  Jinja2 Template    │  ← Renders storyboard HTML
│  (index.html)       │
└─────────────────────┘
         │
         ▼
   Browser (Storyboard)
```

---

## Tech Stack

- **Backend: FastAPI
- **Frontend: HML, CSS (Jinja2)
- **LLM: Groq (Llama 3)
- **Image Generation: Hugging Face (Stable Diffusion XL)
- **NLP: NLTK
- **Env Management: python-dotenv


---

## Project Structure

```
pitch-visualizer/
├── app.py              # FastAPI server — routes & orchestration
├── utils.py            # Core logic: tokenize, refine prompt, generate image
├── requirements.txt    # Python dependencies
├── .env                # API keys (never commit this!)
├── static/             # Static assets folder
│   └── images/         # (reserved for future saved images)
└── templates/
    └── index.html      # Jinja2 storyboard UI
```

---

## Setup & Installation

### Step 1 — Clone / Create the project folder

```bash
mkdir pitch-visualizer && cd pitch-visualizer
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Get your FREE API Keys

**Groq (LLM Prompt Refinement) — Free:**
1. Visit [console.groq.com](https://console.groq.com) → Sign up with Google
2. Go to **API Keys** → **Create API Key**
3. Copy key (starts with `gsk_…`)

**Hugging Face (Image Generation) — Free:**
1. Visit [huggingface.co](https://huggingface.co) → Sign up
2. Go to **Settings → Access Tokens → New Token**
3. Select **Read**, create, copy key (starts with `hf_…`)

### Step 5 — Configure `.env`

```
GROQ_API_KEY=gsk_your_key_here
HF_API_KEY=hf_your_key_here
```

> ⚠️ Never commit `.env` to GitHub. Add it to `.gitignore`.

### Step 6 — Run

```bash
uvicorn app:app --reload
```

Open browser → [http://localhost:8000](http://localhost:8000)

---

## How to Use

1. Type or paste a story (3–6 sentences recommended)
2. Choose a visual style: Cinematic, Digital Art, Watercolor, Noir, 3D/Pixar, or Corporate
3. Click **Generate Storyboard**
4. Wait ~30–60 seconds — each scene is processed individually
5. View your storyboard with image, caption, and the AI-refined prompt for each scene

---

## Prompt Engineering Methodology

This is the core intellectual contribution of the project.

**The Problem:** Raw sentences like `"employees frustrated with manager"` make poor image prompts — they lack visual specificity.

**The Solution — Two-Stage Refinement:**

| Stage | Input | Output |
|---|---|---|
| Raw sentence | "employees frustrated with manager" | (plain text) |
| Style injection | + "cinematic realism" | adds: photorealistic, 35mm film, DSLR |
| LLM enrichment (Groq/Llama-3) | sentence + style hint | "A low-angle shot of a cluttered office, dimly lit with warm overhead glow, casting deep shadows on employees' frustrated faces reflected in windows" |

The system prompt instructs Llama-3 to add: **subject + action + setting + camera angle + lighting mood + color palette** — the six visual dimensions that make image generation prompts effective.

---

## Example Output

**Input story:**
> A startup founder struggled to manage her growing team. The chaos of missed deadlines was costing real money. Employees were frustrated and burning out fast. Then she discovered a simple AI tool. Within weeks, the entire team was thriving.

**Output:** 5 scene cards, each with:
- The original sentence as caption
- AI-engineered cinematic prompt (visible on each card)
- Full Stable Diffusion XL generated image

---

## API Fallback Chain

```
Hugging Face SDXL
      ↓ (if error/timeout)
Pollinations.ai (no key required, always works)
```

This ensures the app always generates images even under API issues.

---

## .gitignore (add this before pushing to GitHub)

```
venv/
.env
__pycache__/
static/images/
*.pyc
```

---

## Dependencies

```
fastapi
uvicorn
jinja2
python-multipart
nltk
requests
python-dotenv
```
