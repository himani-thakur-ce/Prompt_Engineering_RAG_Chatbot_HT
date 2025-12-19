import json
import math

import streamlit as st
import google.generativeai as genai


# ---------- Helpers ----------

def load_api_key() -> str:
    """Load API key from gemini_api.txt"""
    with open("gemini_api.txt", "r", encoding="utf-8") as f:
        key = f.read().strip()
    if not key:
        raise RuntimeError("gemini_api.txt is empty")
    return key


def cosine_similarity(a, b) -> float:
    """Compute cosine similarity between two vectors"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def embed(text: str):
    """Generate an embedding using Google Gemini"""
    resp = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
    )
    return resp["embedding"]


def load_index():
    """Load vector index from pe_index.json"""
    with open("pe_index.json", "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve_relevant_chunks(query: str, k: int = 3):
    """Return top-k most similar chunks"""
    query_emb = embed(query)
    docs = load_index()

    scored = [
        (cosine_similarity(query_emb, doc["embedding"]), doc["text"])
        for doc in docs
    ]

    scored.sort(reverse=True, key=lambda x: x[0])
    return [text for _, text in scored[:k]]


# ---------- Streamlit UI ----------

st.set_page_config(
    page_title="Prompt Engineering Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("Prompt Engineering Chatbot")
st.write("Ask anything about prompt engineering, examples, tips, and best practices.")


@st.cache_resource
def init_gemini():
    """Initialize Gemini generative model"""
    api_key = load_api_key()
    genai.configure(api_key=api_key)

    # ⭐ FIXED: use a model that supports generateContent
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    return model


model = init_gemini()


# ---------- Chat Session ----------

if "messages" not in st.session_state:
    st.session_state.messages = []


user_input = st.chat_input("Ask something about Prompt Engineering...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Retrieve relevant chunks
        chunks = retrieve_relevant_chunks(user_input, k=3)
        context = "\n\n".join(chunks)

        # Build the combined RAG prompt
        prompt = f"""
You are a university-level tutor helping a student prepare for an exam on prompt engineering.

Use ONLY the following context to keep your answer accurate:

CONTEXT:
{context}

USER QUESTION:
{user_input}

Write the answer in the following style:
- Start with a simple 2–3 sentence definition.
- Then give 3–5 bullet points summarizing the key ideas.
- Use very simple, clear English (like explaining to a classmate).
- Do NOT mention section numbers, page numbers, or the word "context".
- Do NOT copy long sentences exactly; rewrite them in your own words.
- Keep the answer short (about 120–180 words).

Now write the answer for the student.
"""


        # Generate response using Gemini
        response = model.generate_content(prompt)
        answer = response.text

    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ---------- Display Chat History ----------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
