# server/app/services/workflow_runner.py
import logging
from typing import Dict, Any, List, Set
from ..config import settings
from ..services.embeddings import query_similar

# Local LLM: use transformers pipeline if requested
local_pipeline = None
if settings.USE_LOCAL_LLM:
    try:
        from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
        logging.info("Loading local LLM: %s", settings.LOCAL_LLM_MODEL)
        # Using text-generation pipeline (works for many causal models)
        local_pipeline = pipeline("text-generation", model=settings.LOCAL_LLM_MODEL, device_map="auto")
    except Exception as e:
        logging.error("Failed to load local LLM: %s", e)
        local_pipeline = None
else:
    local_pipeline = None

def _run_llm(prompt: str, max_new_tokens: int = 256) -> str:
    if local_pipeline:
        out = local_pipeline(prompt, max_new_tokens=max_new_tokens, do_sample=True)
        return out[0].get("generated_text", "").strip()
    # fallback - echo prompt
    logging.warning("No local LLM available, returning prompt as fallback.")
    return "LLM_NOT_AVAILABLE: " + prompt[:1000]

def _get_node_by_id(nodes: List[Dict[str, Any]], nid: str):
    for n in nodes:
        if n["id"] == nid:
            return n
    return None

def _topo_order(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[str]:
    # build adjacency and indegree
    adj = {}
    indeg = {}
    for n in nodes:
        adj[n["id"]] = []
        indeg[n["id"]] = 0
    for e in edges:
        s = e["source"]; t = e["target"]
        adj[s].append(t)
        indeg[t] = indeg.get(t,0)+1
    # Kahn
    q = [n for n in indeg if indeg[n] == 0]
    out = []
    while q:
        u = q.pop(0)
        out.append(u)
        for v in adj.get(u,[]):
            indeg[v]-=1
            if indeg[v]==0:
                q.append(v)
    return out

def run_workflow(workflow: Dict[str, Any], input_query: str = "") -> Dict[str, Any]:
    """
    Run a saved workflow:
    - workflow: { nodes: [...], edges: [...] }
    - nodes have type in node.data.type (or node.type)
    Node types implemented:
      - user: takes input_query
      - kb: runs query_similar to fetch context
      - websearch: placeholder (not implemented)
      - llm: run LLM on built prompt
      - output: collect final text
    Execution follows topological order; for nodes needing inputs it looks at incoming edges.
    """
    nodes = workflow.get("nodes", [])
    edges = workflow.get("edges", [])
    # map node id -> results
    node_outputs = {}
    # Build incoming map
    incoming = {n["id"]: [] for n in nodes}
    outgoing = {n["id"]: [] for n in nodes}
    for e in edges:
        incoming[e["target"]].append(e["source"])
        outgoing[e["source"]].append(e["target"])

    # We'll process nodes in topological order (best-effort)
    order = _topo_order(nodes, edges)
    if not order:
        # fallback to simple nodes order
        order = [n["id"] for n in nodes]

    final_outputs = []
    for nid in order:
        n = _get_node_by_id(nodes, nid)
        if not n:
            continue
        ntype = (n.get("data",{}).get("type") or n.get("type") or n.get("data",{}).get("label","")).lower()
        # Normalize common caret labels
        label = n.get("data",{}).get("label","")
        # Execution per type
        if ntype.startswith("input") or n.get("id","").startswith("user") or "user" in ntype:
            # user node: use input_query
            node_outputs[nid] = {"text": input_query}
        elif "kb" in ntype or "knowledge" in label.lower():
            # get query from incoming node outputs (prefer 1st)
            source_text = ""
            for src in incoming.get(nid,[]):
                s = node_outputs.get(src)
                if s and s.get("text"):
                    source_text = s["text"]; break
            if not source_text:
                source_text = input_query
            # query embeddings DB
            try:
                res = query_similar(source_text, k=3)
                docs = res.get("documents", [[]])[0]
            except Exception as e:
                logging.error("KB query failed: %s", e)
                docs = []
            node_outputs[nid] = {"text": " ".join(docs), "docs": docs}
        elif "websearch" in ntype or "web" in label.lower():
            # placeholder: you can integrate SERP API here; we'll return empty
            node_outputs[nid] = {"text": "", "web": []}
        elif "llm" in ntype or "llm" in label.lower() or "generate" in label.lower() or "engine" in label.lower():
            # Build prompt from incoming nodes: gather context texts from kb nodes etc.
            pieces = []
            for src in incoming.get(nid,[]):
                s = node_outputs.get(src)
                if s and s.get("text"):
                    pieces.append(s["text"])
            # if no incoming, use input_query
            if not pieces:
                pieces = [input_query]
            prompt_prefix = n.get("data",{}).get("prompt","")
            prompt = ""
            if prompt_prefix:
                prompt += prompt_prefix + "\n\n"
            prompt += "Context:\n" + "\n---\n".join(pieces) + "\n\n"
            prompt += f"User Query: {input_query}\nAnswer concisely."
            llm_out = _run_llm(prompt)
            node_outputs[nid] = {"text": llm_out}
        elif "output" in ntype or n.get("id","").startswith("out"):
            # collect incoming outputs
            pieces = []
            for src in incoming.get(nid,[]):
                s = node_outputs.get(src)
                if s and s.get("text"):
                    pieces.append(s["text"])
            combined = "\n\n".join(pieces) if pieces else input_query
            node_outputs[nid] = {"text": combined}
            final_outputs.append({"node": nid, "text": combined})
        else:
            # default: propagate first incoming or input_query
            pieces = []
            for src in incoming.get(nid,[]):
                s = node_outputs.get(src)
                if s and s.get("text"):
                    pieces.append(s["text"])
            node_outputs[nid] = {"text": "\n\n".join(pieces) if pieces else input_query}

    # If output nodes exist, return them; else return last node output
    if final_outputs:
        return {"outputs": final_outputs, "node_outputs": node_outputs}
    else:
        # select last processed node output
        last = order[-1] if order else None
        return {"outputs": [{"node": last, "text": node_outputs.get(last,{}).get("text","")}], "node_outputs": node_outputs}
