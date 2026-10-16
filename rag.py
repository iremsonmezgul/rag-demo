def chunk_text(file_path, chunk_size=500):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


def chunk_by_paragraph(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    paragraphs = text.split("\n\n")

    chunks = []

    for p in paragraphs:
        p = p.strip()
        if p:
            chunks.append(p)

    return chunks

def retrieve(question, chunks):
    question_words = question.lower().split()

    best_chunk = None
    best_score = 0

    for chunk in chunks:
        chunk_words = chunk.lower().split()

        score = 0
        for word in question_words:
            if word in chunk_words:
                score += 1

        if score > best_score:
            best_score = score
            best_chunk = chunk
        
    return best_chunk
            
       

chunks = chunk_by_paragraph("data/bank_faq_tr.txt")
question = "kartımı kaybettim ne yapmalıyım"
answer = retrieve(question, chunks)
print(answer)