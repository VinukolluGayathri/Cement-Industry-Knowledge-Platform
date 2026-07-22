import time
import streamlit as st

# Import backend RAG
from backend.rag import IndustrialRAG


# --------------------------------------------------
# Load RAG only once
# --------------------------------------------------
@st.cache_resource
def load_rag():
    return IndustrialRAG(debug=False)


# --------------------------------------------------
# Chatbot Page
# --------------------------------------------------
def show_chatbot():

    st.header("🤖 Industrial AI Assistant")

    st.markdown("""
Ask questions about:

- 📘 Equipment Manuals
- 📄 SOPs
- ⚙ Maintenance Records
- 🔍 Inspection Reports
- ⚠ Incident Reports
- 📑 Government Regulations
""")

    st.divider()

    rag = load_rag()

    question = st.text_input(
        "Ask your question",
        placeholder="Example: Explain the startup procedure for the Rotary Kiln."
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        ask = st.button("🚀 Ask AI")

    if ask:

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        start = time.time()

        with st.spinner("Searching industrial knowledge base..."):

            try:

                answer, sources, docs = rag.ask(question)

                elapsed = round(time.time() - start, 2)

            except Exception as e:

                st.error(f"Error : {e}")
                return

        # ---------------- Answer ---------------- #

        st.success("Answer")

        st.markdown(answer)

        # ---------------- Sources ---------------- #

        st.divider()

        st.subheader("📄 Source Documents")

        if len(sources) == 0:

            st.info("No supporting documents found.")

        else:

            for source, category in sources:

                icon = "📘"

                if category == "sops":
                    icon = "📄"

                elif category == "maintenance_logs":
                    icon = "⚙"

                elif category == "inspection_reports":
                    icon = "🔍"

                elif category == "incident_reports":
                    icon = "⚠"

                elif category == "regulations":
                    icon = "📑"

                st.write(f"{icon} **{source}**  ({category})")

        st.divider()

        # ---------------- Metrics ---------------- #

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Documents Retrieved", len(docs))

        with col2:
            st.metric("Response Time", f"{elapsed} sec")