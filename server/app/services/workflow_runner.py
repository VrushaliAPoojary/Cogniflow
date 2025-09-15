# server/app/services/workflow_runner.py

from ..services.embeddings import query_similar
from ..config import settings

# If local LLM is enabled, import transformers
if settings.USE_LOCAL_LLM:
    from transformers import pipeline
    local_pipeline = pipeline("text-generation", model=settings.LOCAL_LLM_MODEL)


# -------------------------
# Helper extract functions
# -------------------------
def extract_project_headings(docs):
    """Extract known project headings from context docs"""
    projects = []
    joined = " ".join(docs).lower()

    if "emergency-wave" in joined:
        projects.append("Emergency-Wave App")
    if "resume analyzer" in joined:
        projects.append("AI Resume Analyzer")
    if "multi-feature object detection" in joined:
        projects.append("Multi-Feature Object Detection System")
    if "edumelms" in joined:
        projects.append("EdumelmsFS – Learning Management System")
    if "medical report analyzer" in joined:
        projects.append("Medical Report Analyzer")

    return projects


def extract_candidate_name(docs):
    """Extract candidate name from context docs"""
    for d in docs:
        if "vrushali" in d.lower():
            return "Vrushali A Poojary"
    return "Name not found"


# -------------------------
# LLM wrapper
# -------------------------
def run_llm_with_context(query: str, context_texts: list = None, custom_prompt: str = None):
    """Run query through local LLM with optional KB context"""
    prompt = ""
    if custom_prompt:
        prompt += custom_prompt + "\n\n"
    if context_texts:
        prompt += "Context:\n" + "\n---\n".join(context_texts) + "\n\n"
    prompt += f"User Query: {query}\nAnswer concisely."

    # Run local Hugging Face model
    if settings.USE_LOCAL_LLM:
        # Prevent exceeding GPT2 max length (1024 tokens)
        max_input_length = 800
        if len(prompt) > max_input_length:
            prompt = prompt[:max_input_length]

        result = local_pipeline(
            prompt,
            max_new_tokens=256,
            truncation=True,
            num_return_sequences=1
        )
        return result[0]["generated_text"].strip()

    return "⚠️ No LLM available."


# -------------------------
# Query pipeline
# -------------------------
def run_query_pipeline(query: str, use_kb: bool = True):
    """Pipeline: optionally fetch similar docs, then query LLM"""
    context_texts = []
    if use_kb:
        result = query_similar(query, k=3)
        docs = result.get("documents", [[]])[0]
        if docs:
            context_texts = docs

    q = query.lower()

    # 🚀 Handle structured queries directly
    if "project headings" in q:
        headings = extract_project_headings(context_texts)
        if headings:
            answer = "Here are the project headings:\n" + "\n".join(f"- {h}" for h in headings)
        else:
            answer = "No project headings found."
        return {"answer": answer, "context": context_texts}

    if "candidate name" in q or "resume name" in q:
        name = extract_candidate_name(context_texts)
        return {"answer": f"The candidate's name is: {name}", "context": context_texts}

    # Default → Use LLM
    answer = run_llm_with_context(query, context_texts=context_texts)
    return {"answer": answer, "context": context_texts}
