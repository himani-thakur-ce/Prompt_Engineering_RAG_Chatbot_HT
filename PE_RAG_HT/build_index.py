import json
import google.generativeai as genai

# Load API key
with open("gemini_api.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()

if not api_key:
    raise RuntimeError("gemini_api.txt is empty")

genai.configure(api_key=api_key)

# Read knowledge text
with open("pe_notes.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Very simple chunking: split on double newlines
chunks = [c.strip() for c in raw_text.split("\n\n") if c.strip()]

def embed(text: str):
    resp = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
    )
    return resp["embedding"]

index = []
for chunk in chunks:
    emb = embed(chunk)
    index.append({"text": chunk, "embedding": emb})

with open("pe_index.json", "w", encoding="utf-8") as f:
    json.dump(index, f)

print(f"Saved {len(index)} chunks to pe_index.json")