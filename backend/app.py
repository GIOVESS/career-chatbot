from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import os

# Lightweight model suitable for CPU
MODEL_NAME = "google/flan-t5-small"  # Smallest relevant model for memory efficiency

print("Loading lightweight model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float32,         
    low_cpu_mem_usage=True
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
    inputs = tokenizer(msg.message, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
