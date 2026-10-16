# RAG Demo: Turkish Banking FAQ Assistant

A small Retrieval-Augmented Generation (RAG) project that answers customer questions from a Turkish banking FAQ document, using [sentence-transformers](https://www.sbert.net/) for semantic search and [Google Gemini](https://ai.google.dev/) for answer generation. The FAQ is fictional and was created for this demo.

## How It Works

1. **Chunking:** The document is split into paragraphs, so each question stays with its answer.
2. **Embedding & Retrieval:** The question and chunks are compared by meaning (cosine similarity), and the top-3 chunks are selected.
3. **Confidence check:** If the best score is below 0.5, the system hands the question to a human agent instead of guessing.
4. **Generation:** Gemini writes a short answer using only the retrieved chunks.

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set your [Gemini API key](https://aistudio.google.com) as the `GEMINI_API_KEY` environment variable, then run:

```bash
python rag.py
```

## Example Output

```
SORU: kartımı kaybettim ne yapmalıyım
  (skor: 0.72)
  CEVAP: Merhaba,
  Kartınızı kaybettiyseniz hemen 0850 000 00 00 numaralı müşteri hizmetlerimizi
  arayarak kartınızı kullanıma kapatabilirsiniz. Dilerseniz mobil uygulamamızdaki
  "Kartlarım" menüsünden kartınızı anında geçici olarak dondurabilirsiniz. Kartınız
  kapatıldıktan sonra yeni kartınız ücretsiz olarak adresinize gönderilecektir.
=====
SORU: kartım çalındı
  (skor: 0.66)
  CEVAP: Geçmiş olsun. Kartınızı çaldırdıysanız hemen 0850 000 00 00 numaralı
  müşteri hizmetlerimizi arayarak kartınızı kullanıma kapatabilirsiniz. ...
=====
SORU: başka bankaya para göndermek istiyorum
  Emin değilim (skor: 0.40). Müşteri temsilcisine aktarılıyor.
=====
```
