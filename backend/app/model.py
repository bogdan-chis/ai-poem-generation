from __future__ import annotations

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .settings import settings

_MODEL = None
_TOKENIZER = None
_DEVICE = None

def _pick_device() -> str:
    if settings.DEVICE in ("cpu", "cuda"):
        return settings.DEVICE
    # auto
    if settings.ALLOW_CUDA and torch.cuda.is_available():
        return "cuda"
    return "cpu"

def load_model():
    """
    Loads tokenizer + model once (singleton style).
    """
    global _MODEL, _TOKENIZER, _DEVICE
    if _MODEL is not None and _TOKENIZER is not None:
        return _MODEL, _TOKENIZER, _DEVICE

    _DEVICE = _pick_device()

    _TOKENIZER = AutoTokenizer.from_pretrained(settings.MODEL_DIR, use_fast=True)

    # For GPT2-like models, pad_token often missing; set to eos to avoid warnings.
    if _TOKENIZER.pad_token_id is None:
        _TOKENIZER.pad_token = _TOKENIZER.eos_token

    _MODEL = AutoModelForCausalLM.from_pretrained(
        settings.MODEL_DIR,
        torch_dtype=(torch.float16 if _DEVICE == "cuda" else torch.float32),
    )
    _MODEL.to(_DEVICE)
    _MODEL.eval()

    return _MODEL, _TOKENIZER, _DEVICE

@torch.inference_mode()
def generate_poem(
    title: str,
    max_new_tokens: int = 160,
    do_sample: bool = True,
    temperature: float = 0.9,
    top_p: float = 0.95,
    top_k: int = 50,
    repetition_penalty: float = 1.10,
    no_repeat_ngram_size: int = 3,
    use_title_token: bool = True,
):
    model, tok, device = load_model()

    # If your dataset used "<|title|>" as a control token, this prompt shape matters.
    # Typical training format: "<|title|> Titlu\n" + poem text + "<|endoftext|>"
    if use_title_token and "<|title|>" in tok.get_vocab():
        prompt = f"<|title|> {title}\n"
    else:
        prompt = f"{title}\n"

    inputs = tok(prompt, return_tensors="pt").to(device)

    out_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temperature if do_sample else None,
        top_p=top_p if do_sample else None,
        top_k=top_k if do_sample else None,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        eos_token_id=tok.eos_token_id,
        pad_token_id=tok.eos_token_id,
    )

    text = tok.decode(out_ids[0], skip_special_tokens=True)

    # Often the decoded output includes the title line; keep it, but you can strip if you prefer.
    return prompt, text, device
