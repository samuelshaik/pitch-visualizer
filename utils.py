
import nltk, requests, os, base64
from dotenv import load_dotenv

load_dotenv()

nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)

GROQ_KEY = os.getenv("GROQ_API_KEY", "")
HF_KEY   = os.getenv("HF_API_KEY",   "")

# Style keyword map 
STYLE_HINTS = {
    "cinematic realism":       "photorealistic, cinematic lighting, DSLR, 35mm film",
    "digital art illustration": "digital art, concept art, vivid colors, detailed brushwork",
    "watercolor painting":     "watercolor painting, soft edges, pastel tones, artistic",
    "noir film photography":   "black and white, dramatic shadows, film noir, high contrast",
    "3D render Pixar style":   "3D render, Pixar animation style, vibrant, expressive characters",
    "flat vector corporate art":"flat design, vector art, clean lines, corporate infographic style",
}

#  1. Sentence tokenizer 
def split_text(text: str) -> list[str]:
    from nltk.tokenize import sent_tokenize
    raw = sent_tokenize(text.strip())
    return [s.strip() for s in raw if len(s.strip()) > 8][:6]


# ── 2. LLM prompt refinement (Groq — free) 
def enhance_prompt(sentence: str, style: str = "cinematic realism") -> str:
    style_hint = STYLE_HINTS.get(style, style)

    # Fallback when no key
    if not GROQ_KEY:
        return (
            f"Storyboard panel: {sentence}. "
            f"Style: {style_hint}. "
            "Ultra detailed, professional composition, dramatic lighting."
        )

    system = (
        "You are a world-class visual storyboard director. "
        "Given a plain sentence, produce ONE highly detailed image-generation prompt. "
        f"Apply this visual style: '{style}' ({style_hint}). "
        "Include: subject, action, setting, camera angle, lighting mood, color palette. "
        "Output ONLY the prompt — no quotes, no labels, no explanation. Max 70 words."
    )
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}",
                     "Content-Type": "application/json"},
            json={
                "model": "llama-3.1-8b-instant",
                "max_tokens": 160,
                "temperature": 0.85,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": f"Scene: {sentence}"},
                ],
            },
            timeout=15,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[Groq error] {e}")
        return (
            f"Storyboard panel: {sentence}. "
            f"Style: {style_hint}. Dramatic composition, professional lighting."
        )


# 3. Image generation (huggingface)
def _pollinations(prompt: str) -> str:
    safe = requests.utils.quote(prompt[:500])
    return f"https://image.pollinations.ai/prompt/{safe}?width=800&height=600&nologo=true&enhance=true"


def generate_image(prompt: str) -> str:
    if not HF_KEY:
        print("[Image] No HF key — using Pollinations")
        return _pollinations(prompt)

    try:
        r = requests.post(
            "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
            headers={"Authorization": f"Bearer {HF_KEY}"},
            json={"inputs": prompt},
            timeout=90,
        )
        if r.status_code == 200:
            return "data:image/jpeg;base64," + base64.b64encode(r.content).decode()
        print(f"[HF {r.status_code}] falling back to Pollinations")
    except Exception as e:
        print(f"[HF error] {e}")

    return _pollinations(prompt) 