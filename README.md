<div align="center">

# 🎓 SQLGenie

### Ask your student database a question in plain English.

<img src="https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/LangChain-🦜🔗-1C3C3C?style=for-the-badge">
<img src="https://img.shields.io/badge/Groq-Llama_3.3-F55036?style=for-the-badge&logo=groq&logoColor=white">
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white">

</div>

---

**"What's Ali's weighted GPA?"** · **"Who's on academic probation?"**

Type a question like you'd ask a person. SQLGenie turns it into real SQL, runs it against MySQL, and answers back.

## 🧠 Architecture

```
Question ──▶ Retrieve similar examples (Chroma + embeddings)
         ──▶ LLM writes SQL 
         ──▶ Query runs on MySQL
         ──▶ Answer
```

- **`SQLDatabase`** reads your schema so the LLM knows the tables
- **Prompt prefix** encodes business rules the schema can't (grade→point mapping, probation cutoff, weighted GPA formula)
- **Few-shots + embeddings** teach query *patterns* — joins, aggregations — retrieved per question, not dumped in wholesale
- **Chain** stitches it all together and executes the final SQL

## ⚡ Quickstart

```bash
pip install -r requirements.txt --break-system-packages
```

```env
GROQ_API_KEY=your_key_here
```

```bash
streamlit run main.py
```

## 🗂️ Files

| File | Role |
|---|---|
| `main.py` | 🎈 Streamlit UI |
| `langchain_helper.py` | 🧠 Prompt + chain + LLM setup |
| `few_shots.py` | 📚 Example queries the model learns from |

## 💬 Try Asking

```
What is the CGPA of Bilal Ahmed?
Which students got an F grade?
What is the weighted GPA of Ali Raza?
```

---

<div align="center">Built with 🦜🔗 LangChain · ⚡ Groq · 🐬 MySQL</div>
