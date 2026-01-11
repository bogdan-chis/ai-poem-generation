from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import GenerateRequest, GenerateResponse
from .model import generate_poem, load_model

app = FastAPI(title="Nichita Poem Generator API", version="1.0.0")

# React dev server defaults to http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    # Preload model at startup so first request isn't slow
    load_model()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    prompt, text, device = generate_poem(
        title=req.title,
        max_new_tokens=req.max_new_tokens,
        do_sample=req.do_sample,
        temperature=req.temperature,
        top_p=req.top_p,
        top_k=req.top_k,
        repetition_penalty=req.repetition_penalty,
        no_repeat_ngram_size=req.no_repeat_ngram_size,
        use_title_token=req.use_title_token,
    )
    return GenerateResponse(prompt=prompt, text=text, device=device)
