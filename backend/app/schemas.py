from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    # Generation controls (sane defaults)
    max_new_tokens: int = Field(160, ge=16, le=512)
    do_sample: bool = True
    temperature: float = Field(0.9, ge=0.1, le=2.0)
    top_p: float = Field(0.95, ge=0.1, le=1.0)
    top_k: int = Field(50, ge=0, le=200)

    # Repetition controls
    repetition_penalty: float = Field(1.10, ge=1.0, le=2.0)
    no_repeat_ngram_size: int = Field(3, ge=0, le=10)

    # If you trained with "<|title|>" prompting, keep this on:
    use_title_token: bool = True

class GenerateResponse(BaseModel):
    prompt: str
    text: str
    device: str
