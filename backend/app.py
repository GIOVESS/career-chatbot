from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

MODEL_NAME = "microsoft/phi-2"     # we'll swap to "mistralai/Mistral-7B-Instruct" if GPU available

print("Loading model... this may take a minute ")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve static frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

class Message(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(msg: Message):
    inputs = tokenizer(msg.message, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
