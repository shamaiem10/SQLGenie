from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from few_shots import few_shots
from dotenv import load_dotenv
import os

load_dotenv()


def get_few_shot_db_chain():
    db_user = "root"
    db_password = "root"      
    db_host = "localhost"
    db_name = "university_records"

    db = SQLDatabase.from_uri(
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}",
        sample_rows_in_table_info=3
    )

    llm = ChatGroq(
        groq_api_key=os.environ["GROQ_API_KEY"],
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    to_vectorize = [" ".join(example.values()) for example in few_shots]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma.from_texts(
        to_vectorize,
        embeddings,
        metadatas=few_shots
    )

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=3
    )

    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically 
correct MySQL query to run, then look at the results of the query and return 
the answer to the input question.

Unless the user specifies a number of results, limit to at most {top_k} results 
using LIMIT.

Never query all columns — only the ones needed. Wrap column names in backticks.

Pay attention to which column belongs to which table. The `students` table holds 
one row per student (cgpa, department, semester = the student's current semester). 
The `enrollments` table holds one row per course a student has taken (grade, 
credit_hours, and its own semester = the semester that specific course was taken in) 
and links to `students` via student_id.

If a question mentions "semester" without saying "current semester" or "enrolled in", 
assume it refers to the enrollment's semester (which course was taken when), not the 
student's overall semester.

Grade-to-point conversion when GPA calculations are asked for: 
A=4.0, B=3.0, C=2.0, D=1.0, F=0.0.

"Academic probation" means CGPA below 2.5, unless the question specifies a 
different threshold.

Weighted GPA means SUM(grade_point * credit_hours) / SUM(credit_hours), 
not a plain average of grades.

No pre-amble.
...
No pre-amble.

Return ONLY the SQL query.

Do NOT wrap the SQL in markdown.

Do NOT use ```sql or ```.

Output plain SQL text only."""

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="Question: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"]
    )

    chain = SQLDatabaseChain.from_llm(
        llm, db, verbose=True, prompt=few_shot_prompt
    )

    return chain