from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import torch
import nest_asyncio
import os

app = FastAPI()

device = 0 if torch.cuda.is_available() else -1
print(f"Using device: {'CUDA (GPU)' if device == 0 else 'CPU'}")

text_generator = pipeline(
    "text-generation",
    model="Llama-2-7b-hf",
    #device=device
    device=0
)

class TextRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 100
    temperature: float = 0.7

@app.post("/generate/")
async def generate_text(request: TextRequest):
    output = text_generator(
        request.prompt,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        return_full_text=False
    )
    return {"generated_text": output[0]["generated_text"]}

if __name__ == "__main__":
    import uvicorn
    nest_asyncio.apply()
    CDSW_APP_PORT = os.getenv("CDSW_APP_PORT", 8100)
    uvicorn.run(app, host="127.0.0.1", port=int(CDSW_APP_PORT))
