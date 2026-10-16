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


chunks = chunk_by_paragraph("data/bank_faq_tr.txt")
print(len(chunks))
for c in chunks:
    print("---")
    print(c)