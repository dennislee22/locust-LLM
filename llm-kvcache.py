from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import nest_asyncio

app = FastAPI()

model_name = "Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

kv_cache = {}

class TextRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50
    temperature: float = 0.7
    cache_key: str = None
    use_cache: bool = True

@app.post("/generate/")
async def generate_text(request: TextRequest):
    global kv_cache

    input_ids = tokenizer(request.prompt, return_tensors="pt").input_ids.to(device)

    past_key_values = None
    if request.use_cache and request.cache_key and request.cache_key in kv_cache:
        past_key_values = kv_cache[request.cache_key]

    outputs = model.generate(
        input_ids,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        use_cache=request.use_cache,
        past_key_values=past_key_values,
        return_dict_in_generate=True,
        output_scores=False
    )

    generated = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)

    if request.use_cache and request.cache_key:
        kv_cache[request.cache_key] = outputs.past_key_values

    return {"generated_text": generated}

if __name__ == "__main__":
    import uvicorn
    nest_asyncio.apply()
    CDSW_APP_PORT = os.getenv("CDSW_APP_PORT", 8100)
    uvicorn.run(app, host="127.0.0.1", port=int(CDSW_APP_PORT))
