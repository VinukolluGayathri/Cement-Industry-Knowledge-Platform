import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class IndustrialRAG:

    def __init__(self, debug=False):

        self.debug = debug

        # ---------------- Embedding Model ---------------- #
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # ---------------- Vector Database ---------------- #
        self.vector_db = Chroma(
            persist_directory="database/chroma_db",
            embedding_function=self.embeddings
        )

        # ---------------- Gemini LLM ---------------- #
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0.2
        )

        # ---------------- Default Retriever ---------------- #
        self.retriever = self.vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 20
            }
        )

        # ---------------- Prompt ---------------- #
        self.prompt = ChatPromptTemplate.from_template("""
You are an AI-powered Industrial Knowledge Assistant for a Cement Manufacturing Plant.

You answer questions ONLY using the information provided in the retrieved context.

Your knowledge base consists of:
- Equipment Manuals
- Standard Operating Procedures (SOPs)
- Maintenance Logs
- Inspection Reports
- Incident Reports
- Safety Regulations

Instructions:

1. NEVER invent, assume, or hallucinate any information.
2. Base every answer strictly on the retrieved context.
3. If multiple documents contain relevant information, combine them into a single well-structured answer.
4. If only partial information is available, clearly state that the answer is based on the available information and summarize it.
5. If no relevant information exists in the retrieved context, reply EXACTLY:

"I couldn't find this information in the knowledge base."

6. Whenever applicable, include:
   • Equipment Name
   • Equipment ID
   • Maintenance Date
   • Inspection Date
   • Work Order ID
   • Failure Mode
   • Root Cause
   • Action Taken
   • Recommendations
   • Operating Parameters

7. For procedure-related questions:
   - Present the steps in the correct sequence.
   - Preserve important operating values such as temperature, pressure, RPM, feed rate, flow rate, etc.
   - Do not omit safety-related steps.

8. For maintenance-related questions:
   Include:
   - Maintenance Type
   - Failure Mode
   - Root Cause
   - Corrective / Preventive Action
   - Spare Parts Used
   - Technician
   - Downtime
   - Status
   - Recommendations

9. For inspection-related questions:
   Include:
   - Inspection Type
   - Inspection Date
   - Measured Parameters
   - Findings
   - Result (Pass/Fail)
   - Recommended Actions

10. For incident-related questions:
    Include:
    - Incident Type
    - Severity
    - Root Cause
    - Immediate Actions
    - Corrective Actions
    - Current Status

11. For equipment-related questions:
    Explain:
    - Purpose
    - Function
    - Working principle (only if present in the context)
    - Important operating conditions
    - Important precautions

12. Whenever safety information exists in the retrieved context, always include a separate section:

### Safety Precautions

13. Use professional industrial engineering language.

14. Organize the answer using Markdown headings and bullet points whenever appropriate.

15. Never mention information that is not present in the retrieved documents.

16. Do not mention internal implementation details such as embeddings, vector databases, retrieval, or AI models.

17. If the retrieved context comes from multiple documents, naturally combine the information instead of describing each document separately.

----------------------------
Retrieved Context
----------------------------

{context}

----------------------------
User Question
----------------------------

{question}

----------------------------
Answer
----------------------------
""")

    # -------------------------------------------------------------

    def retrieve_documents(self, question):

        q = question.lower()

        procedure_keywords = [
            "start",
            "startup",
            "procedure",
            "shutdown",
            "sop",
            "steps",
            "operate",
            "operation"
        ]

        if any(word in q for word in procedure_keywords):

            docs = self.vector_db.similarity_search(
                question,
                k=8,
                filter={"category": "sops"}
            )

            if docs:
                return docs

        return self.retriever.invoke(question)

    # -------------------------------------------------------------

    def build_context(self, docs):

        context = []

        for doc in docs:

            source = doc.metadata.get("source", "Unknown")
            category = doc.metadata.get("category", "Unknown")

            context.append(
                f"""
                    Source : {source}
                    Category : {category}

                    {doc.page_content}
                """
            )

        return "\n\n".join(context)

    # -------------------------------------------------------------

    def ask(self, question):

        docs = self.retrieve_documents(question)

        if len(docs) == 0:

            return (
                "I couldn't find this information in the knowledge base.",
                [],
                []
            )

        context = self.build_context(docs)

        messages = self.prompt.invoke(
            {
                "context": context,
                "question": question
            }
        )

        try:

            response = self.llm.invoke(messages)

            if isinstance(response.content, list):

                answer = ""

                for item in response.content:

                    if isinstance(item, dict):

                        if item.get("type") == "text":
                            answer += item.get("text", "")

                    else:
                        answer += str(item)

            else:
                answer = response.content

        except Exception as e:

            answer = f"LLM Error: {str(e)}"

        # ---------- Sources ----------

        sources = []

        for doc in docs:

            src = (
                doc.metadata.get("source"),
                doc.metadata.get("category")
            )

            if src not in sources:
                sources.append(src)

        return answer.strip(), sources, docs


# =====================================================================

if __name__ == "__main__":

    rag = IndustrialRAG(debug=True)

    while True:

        question = input("\nAsk Question (type exit to quit): ")

        if question.lower() == "exit":
            break

        answer, sources, docs = rag.ask(question)

        # ---------------- Debug ---------------- #

        if rag.debug:

            print("\n" + "=" * 90)
            print("RETRIEVED DOCUMENTS")
            print("=" * 90)

            for i, doc in enumerate(docs, 1):

                print(f"\nDocument {i}")
                print("-" * 90)
                print("Metadata :", doc.metadata)
                print(doc.page_content[:700])
                print("-" * 90)

        # ---------------- Answer ---------------- #

        print("\n" + "=" * 80)
        print("ANSWER")
        print("=" * 80)
        print(answer)

        print("\nSources Used:")

        for source, category in sources:
            print(f"• {source} ({category})")