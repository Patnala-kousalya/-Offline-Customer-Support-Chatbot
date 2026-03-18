import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

def load_template(path):
    with open(path, "r") as f:
        return f.read()

def query_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "").strip()

queries = [
    "How do I track my order?",
    "My discount code is not working.",
    "Can I cancel my order?",
    "How long does delivery take?",
    "Where can I see my order history?",
    "Do you offer cash on delivery?",
    "My payment failed but money was deducted.",
    "How do I return a product?",
    "Can I exchange my item?",
    "Do you ship internationally?",
    "I received a damaged product.",
    "How do I update my address?",
    "What payment methods do you accept?",
    "My order is delayed.",
    "Can I change my order after placing it?",
    "How do I contact support?",
    "Is there any warranty on products?",
    "How do I apply a coupon?",
    "My account is locked.",
    "I didn’t receive order confirmation."
]

zero_template = load_template("prompts/zero_shot_template.txt")
one_template = load_template("prompts/one_shot_template.txt")

with open("eval/results.md", "w", encoding="utf-8") as f:
    f.write("| Query | Method | Response | Relevance | Coherence | Helpfulness |\n")
    f.write("|-------|--------|----------|-----------|-----------|-------------|\n")

    for q in queries:
        z_prompt = zero_template.replace("{query}", q)
        o_prompt = one_template.replace("{query}", q)

        z_res = query_ollama(z_prompt)
        o_res = query_ollama(o_prompt)

        f.write(f"| {q} | Zero-shot | {z_res} |  |  |  |\n")
        f.write(f"| {q} | One-shot | {o_res} |  |  |  |\n")