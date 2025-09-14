# server/app/services/workflow_runner.py
from ..services.embeddings import query_similar
from openai import OpenAI
from ..config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def run_llm_with_context(query: str, context_texts: list = None, custom_prompt: str = None):
    """Run query through LLM with optional KB context"""
    prompt = ""
    if custom_prompt:
        prompt += custom_prompt + "\n\n"
    if context_texts:
        prompt += "Context:\n" + "\n---\n".join(context_texts) + "\n\n"
    prompt += f"User Query: {query}\nAnswer concisely."

    # ✅ New OpenAI API
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # switch to gpt-3.5-turbo if needed
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def run_query_pipeline(query: str, use_kb: bool = True):
    """Pipeline: optionally fetch similar docs, then query LLM"""
    context_texts = []
    if use_kb:
        result = query_similar(query, k=3)
        docs = result.get("documents", [[]])[0]
        if docs:
            context_texts = docs
    answer = run_llm_with_context(query, context_texts=context_texts)
    return {"answer": answer, "context": context_texts}
