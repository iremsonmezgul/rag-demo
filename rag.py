from sentence_transformers import SentenceTransformer, util
from google import genai


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


def retrieve_semantic(question, chunks, model, top_k=3):
    chunk_embeddings = model.encode(chunks)
    question_embedding = model.encode(question)

    scores = util.cos_sim(question_embedding, chunk_embeddings)[0]

    top_results = scores.topk(top_k)

    results = []
    for score, index in zip(top_results.values, top_results.indices):
        results.append((chunks[int(index)], float(score)))

    return results
 

def generate_answer(question, context_chunks, client):
    context = "\n\n".join(context_chunks)

    prompt = f"""Sen Örnek Bank'ın müşteri hizmetleri asistanısın.
Aşağıdaki bilgilere dayanarak müşterinin sorusunu kısa ve nazik bir şekilde cevapla.
Cevap bilgilerde yoksa bilmediğini söyle, bilgi uydurma.

Bilgiler:
{context}

Soru: {question}
Cevap:"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )
    return interaction.output_text


model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = genai.Client()
chunks = chunk_by_paragraph("data/bank_faq_tr.txt")

THRESHOLD = 0.5

questions = [
    "kartımı kaybettim ne yapmalıyım",
    "kartım çalındı",
    "başka bankaya para göndermek istiyorum",
]

for q in questions:
    print("SORU:", q)
    results = retrieve_semantic(q, chunks, model)

    best_chunk, best_score = results[0]

    if best_score < THRESHOLD:
        print(f"  Emin değilim (skor: {best_score:.2f}). Müşteri temsilcisine aktarılıyor.")
    else:
        context_chunks = [chunk for chunk, score in results]
        answer = generate_answer(q, context_chunks, client)
        print(f"  (skor: {best_score:.2f})")
        print("  CEVAP:", answer)

    print("=====")