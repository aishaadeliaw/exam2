import re

def chunk_by_sentences(text: str, max_chars: int = 8000):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = []
    current_length = 0
    start_index = 0
    
    for i, sentence in enumerate(sentences):

        if current_length + len(sentence) + 1 > max_chars:

            chunk_text = " ".join(current_chunk)
            chunks.append({
                "header": f"Sentences {start_index + 1}–{i}",
                "content": chunk_text
            })

            current_chunk = [sentence]
            current_length = len(sentence)
            start_index = i

        else:
            current_chunk.append(sentence)
            current_length += len(sentence) + 1

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "header": f"Sentences {start_index + 1}–{len(sentences)}",
            "content": chunk_text
        })

    return chunks