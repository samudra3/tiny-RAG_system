# 🔍 Tiny RAG System

> **RAG from scratch, in the simplest form possible.**
> Most of the logic is written by hand, with no magic framework hiding what is going on, so you can see exactly how a RAG system works.

---

## 📖 Table of Contents

1. [What does RAG mean?](#-what-does-rag-mean)
2. [RAG is a pipeline, not a library](#-rag-is-a-pipeline-not-a-library)
3. [The three words: Retrieval, Augmented, Generation](#-the-three-words-retrieval-augmented-generation)
4. [Project structure](#-project-structure)
5. [Step-by-step: how the pipeline is built in this project](#-step-by-step-how-the-pipeline-is-built-in-this-project)
6. [Retrieval technique and cosine similarity](#-retrieval-technique-and-cosine-similarity)
7. [Upgrade: from manual search to a vector database](#-upgrade-from-manual-search-to-a-vector-database)
8. [How to run](#-how-to-run)
9. [Tech used](#-tech-used)
10. [Known limitations](#-known-limitations)

---

## 🧠 What does RAG mean?

**RAG** stands for **R**etrieval-**A**ugmented **G**eneration.

In one line: *RAG lets an AI answer questions using **your own documents**, instead of only what it memorised during training.*

### The problem it solves

An AI model (like Gemini or ChatGPT) has never read your company policy, your notes or your private files. If you ask it *"How many days can I work from home?"*, it will either say "I don't know" or, worse, **make something up**.

### The idea behind the solution

Think of an **open-book exam**:

| Closed-book exam | Open-book exam (RAG) |
|---|---|
| The student answers only from memory | The student first **finds the right page** in the book, then answers using it |
| Might guess or be wrong | Answers are grounded in the real source |

RAG does the same thing with an AI: **find the right pieces of your document first, hand them to the AI, and then let it answer.**

---

## 🔗 RAG is a pipeline, not a library

A very common misunderstanding is that RAG is a package you `pip install`. **It is not.**

> **RAG is a *sequence of steps* (a pipeline). The output of one step becomes the input of the next.**

Libraries like ChromaDB or the Gemini SDK are just *tools* we use inside some of the steps. The idea itself is the order of the steps:

```
 📄 Document
     │
     ▼
 ① Load the text
     │
     ▼
 ② Chunk  ───────► cut the text into small pieces
     │
     ▼
 ③ Embed  ───────► turn each piece into numbers (a vector)
     │
     ▼
 ④ Store  ───────► keep those vectors in a database
     │
     ▼        ❓ User asks a question
     │                │
     │                ▼
     │        ⑤ RETRIEVE ──► find the chunks closest to the question
     │                │
     │                ▼
     │        ⑥ AUGMENT  ──► paste those chunks + question into a prompt
     │                │
     │                ▼
     │        ⑦ GENERATE ──► the AI writes the final answer
     │                │
     ▼                ▼
                 ✅ Answer
```

Steps ①–④ are done **once** (preparing the knowledge). Steps ⑤–⑦ run **every time** someone asks a question.

---

## 🧩 The three words: Retrieval, Augmented, Generation

### 1️⃣ Retrieval = "Go and find it"
Search through your documents and **fetch only the few pieces that are relevant** to the question.
*Like using the index at the back of a book to jump straight to the right page.*

📂 **In this project:** [`retrieval.py`](retrieval.py)

### 2️⃣ Augmented = "Add it to the question"
*Augment* simply means **to add or enrich**. We take the pieces we found and **add them to the question** inside a prompt, so the AI sees the question *together with* the useful information.
*Like stapling the relevant book pages to the exam question before handing it over.*

📂 **In this project:** [`prompt_builder.py`](prompt_builder.py)

### 3️⃣ Generation = "Write the answer"
The AI model reads the prompt (question + found information) and **generates a natural-language answer**.
*Like the student reading the pages and writing the answer in their own words.*

📂 **In this project:** [`generation.py`](generation.py)

---

## 📁 Project structure

```
tiny-RAG_system/
│
├── documents/
│   └── remote-work.txt     # The knowledge source (our "book")
│
├── chunk.py                # Step ②  Cut the document into chunks
├── embed.py                # Step ③  Convert text → vector (numbers)
├── chroma_test.py          # Step ④  Vector database (ChromaDB) setup
├── retrieval.py            # Step ⑤  RETRIEVAL  (cosine similarity + vector DB search)
├── prompt_builder.py       # Step ⑥  AUGMENTATION (build the prompt)
├── generation.py           # Step ⑦  GENERATION (ask the AI model)
├── main.py                 # The "conductor" that runs the whole pipeline
└── requirements.txt        # Python dependencies
```

---

## 🪜 Step-by-step: how the pipeline is built in this project

### ① Load the document : `main.py`
We read a plain text file, `documents/remote-work.txt`, which is the knowledge we want the AI to use.

### ② Chunking : [`chunk.py`](chunk.py)
**What:** Cut the long document into small pieces called **chunks**.
**Why:** Searching a whole document is too coarse. Small pieces let us pick *exactly* the part that answers the question, and keep the prompt short.

**How it is done here (by hand):** the text is split into paragraphs, and paragraphs are joined together until a chunk reaches the size limit (`chunk_size`). Then a new chunk starts.

### ③ Embedding : [`embed.py`](embed.py)
**What:** Convert each chunk of text into a list of numbers called a **vector** (or *embedding*).
**Why:** Computers can't compare *meaning* directly, but they can compare numbers. Text with similar meaning gets similar numbers.

> 💡 Example: "work from home" and "remote working" use different words but mean the same thing, so their vectors end up **close together**.

We use Google's **`gemini-embedding-2`** model for this.

### ④ Storing : [`chroma_test.py`](chroma_test.py)
**What:** Save every chunk, its vector and its source into a **vector database** (ChromaDB), stored on disk in the `chroma-db/` folder.
**Why:** So we don't have to re-read and re-embed the document every time.

### ⑤ Retrieval : [`retrieval.py`](retrieval.py) ← the **R** in RAG
1. The user's **question** is turned into a vector using the *same* embedding model.
2. The question vector is compared with the chunk vectors.
3. The **top 2 closest chunks** (`n_chunks=2`) are returned.

### ⑥ Augmentation : [`prompt_builder.py`](prompt_builder.py) ← the **A** in RAG
The retrieved chunks and the question are stitched into one prompt:

```
you have to answer using the provided context

context:
<chunk 1>
<chunk 2>
Question:
How many days can I work from home?

answer only using provided context
```

The instruction *"answer only using provided context"* keeps the AI honest and stops it from inventing facts.

### ⑦ Generation : [`generation.py`](generation.py) ← the **G** in RAG
The final prompt is sent to Google's **Gemini** model (`gemini-3.5-flash-lite`), which writes the answer.

---

## 📐 Retrieval technique and cosine similarity

### What retrieval technique is used?

**Semantic (meaning-based) search using vector embeddings, returning the Top-K most similar chunks** (here K = 2).

It is *not* simple keyword matching. It finds chunks by **meaning**, even when the exact words differ.

### How does the computer decide "which chunk is closest"?

Using **cosine similarity**.

#### The simple picture 🧭
Imagine every piece of text as an **arrow** pointing in some direction in space.

- If two arrows point in **nearly the same direction** → the texts have **similar meaning** → score close to **1**
- If they point in **completely different directions** → unrelated → score close to **0**

Cosine similarity measures the **angle** between the two arrows.

```
Question ➚      Chunk A ➚   → small angle → HIGH score  ✅ relevant
Question ➚      Chunk B ➙   → big angle   → LOW score   ❌ not relevant
```

#### The formula (written by hand in this project)

```
                 A · B
cosine = ─────────────────────
          ‖A‖  ×  ‖B‖
```

```python
def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

- `np.dot(a, b)` multiplies the two vectors position by position and adds it all up.
- `np.linalg.norm(a)` is the "length" of an arrow.
- Dividing by the lengths means only the **direction** matters, not how long the text was.

#### The manual retrieval process (version 1)

1. Embed the question → `question_vector`
2. For **every** chunk, compute `cosine_similarity(question_vector, chunk_vector)`
3. **Sort** the chunks from highest to lowest score
4. Keep the **top 2**

This is the "brute force" approach: simple, easy to understand, and perfect for learning. You can still see this logic preserved as comments inside [`retrieval.py`](retrieval.py).

---

## 🚀 Upgrade: from manual search to a vector database

**Version 1: manual (in memory)**
All chunk vectors lived in a Python list. Each question compared against *every* chunk one by one. It works great for a handful of chunks, but gets slow as documents grow, and everything disappears when the program stops.

**Version 2: vector database (ChromaDB)** ← *current*
We moved the vectors into **ChromaDB**:

| | Manual list | Vector database |
|---|---|---|
| Storage | In memory (lost on exit) | Saved on disk (`chroma-db/`) |
| Searching | Compare against every chunk | Optimised search built for vectors |
| Scales to big data | ❌ | ✅ |
| Embed documents once | ❌ (re-done every run) | ✅ (stored and reused) |

The retrieval step now becomes one line:

```python
results = collection.query(query_embeddings=[query_vector], n_results=2)
```

> ⚠️ **The pipeline did not change. Only the "how" inside the Retrieval step changed.** This is the key point of RAG being a *pipeline*: you can swap out any single step without breaking the others.

---

## ▶️ How to run

### 1. Clone the repo
```bash
git clone https://github.com/samudra3/tiny-RAG_system.git
cd tiny-RAG_system
```

### 2. Install the requirements
```bash
pip install -r requirements.txt
pip install python-dotenv
```

### 3. Add your Gemini API key
Create a file named `.env` in the project root:
```
GEMINI_API_KEY=your_api_key_here
```
Get a free key from [Google AI Studio](https://aistudio.google.com/).

### 4. Fill the vector database (first run only)
In `main.py`, un-comment the `collection.add(...)` loop so the chunks are stored in ChromaDB, run the project once, then comment it again so chunks are not added twice.

### 5. Run
```bash
python main.py
```

By default, `main.py` retrieves the best chunks for the question and prints the final **augmented prompt**, so you can *see* exactly what the AI would receive. To get the final AI answer, un-comment the generation lines:

```python
answer = generate_response(prompt)
print(answer)
```

---

## 🛠 Tech used

| Purpose | Tool |
|---|---|
| Language | Python |
| Embeddings | Google Gemini (`gemini-embedding-2`) via `google-genai` |
| Answer generation | Google Gemini (`gemini-3.5-flash-lite`) via `google-genai` |
| Vector database | ChromaDB |
| Math (cosine similarity) | NumPy |

---

## ⚠️ Known limitations

This is a **learning project**, kept intentionally small:

- The chunking is simple (by paragraph and size). Real systems often use smarter splitting and overlap between chunks.
- It reads a single text file.
- ChromaDB uses its own default distance measure for ranking unless it is configured for cosine; the hand-written `cosine_similarity` function is there to show the concept explained above.
- There is no user interface; everything runs from the terminal.

---

## 🎯 Key takeaway

> **RAG = Retrieve the right information → Augment the prompt with it → Generate the answer.**
> Three simple steps in a pipeline, with no magic involved.

---

⭐ If this project helped you understand RAG, consider giving it a star!