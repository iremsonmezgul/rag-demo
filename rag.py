from sentence_transformers import SentenceTransformer, util


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
        if len(p) > 80:
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


def retrieve_semantic(question, chunks, model):
    chunk_embeddings = model.encode(chunks)
    question_embedding = model.encode(question)

    scores = util.cos_sim(question_embedding, chunk_embeddings)[0]

    best_index = int(scores.argmax())
    return chunks[best_index], float(scores[best_index])            
       

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
chunks = chunk_by_paragraph("data/bank_faq_tr.txt")

questions = [
    "kartımı kaybettim ne yapmalıyım",
    "kartım çalındı",
    "başka bankaya para göndermek istiyorum",
]

for q in questions:
    print("SORU:", q)
    print("KELİME ARAMASI:", retrieve(q, chunks))
    answer, score = retrieve_semantic(q, chunks, model)
    print("EMBEDDING ARAMASI:", answer)
    print("BENZERLİK SKORU:", round(score, 2))
    print("=====")