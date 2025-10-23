import re

def chunk_by_sentences(text: str, n: int = 30):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    for i in range(0, len(sentences), n):
        chunk = sentences[i:i+n]
        chunks.append({
            "header": f"Sentences {i+1}–{i+len(chunk)}",
            "content": " ".join(chunk)
        })

    return chunks