import google.generativeai as genai

# Load your API key from gemini_api.txt
with open("gemini_api.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()

if not api_key:
    raise RuntimeError("gemini_api.txt is empty")

genai.configure(api_key=api_key)

print("Available models that support generateContent:\n")
for m in genai.list_models():
    methods = getattr(m, "supported_generation_methods", []) or []
    if "generateContent" in methods:
        print("-", m.name)
