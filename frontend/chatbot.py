import time
from collections import Counter

import streamlit as st

from backend.rag import IndustrialRAG


# ------------------------------------------------------------
# Load RAG only once
# ------------------------------------------------------------

@st.cache_resource
def load_rag():
    return IndustrialRAG(debug=False)


# ------------------------------------------------------------
# Helper Function
# ------------------------------------------------------------

def get_icon(category):

    icons = {
        "manuals": "📘",
        "sops": "📄",
        "maintenance_logs": "⚙️",
        "inspection_reports": "🔎",
        "incident_reports": "⚠️",
        "regulations": "📑"
    }

    return icons.get(category, "📄")


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

def sidebar():

    st.sidebar.title("🏭 Cement Industry AI")

    st.sidebar.success("Backend Connected")

    st.sidebar.markdown("---")

    st.sidebar.subheader("⚙ System Information")

    st.sidebar.write("**LLM** : Gemini Flash")
    st.sidebar.write("**Embeddings** : MiniLM-L6-v2")
    st.sidebar.write("**Vector DB** : ChromaDB")
    st.sidebar.write("**Knowledge Base** : Cement Plant")

    st.sidebar.markdown("---")

    if st.sidebar.button("🗑 Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# ------------------------------------------------------------
# Chatbot Page
# ------------------------------------------------------------

def show_chatbot():

    sidebar()

    rag = load_rag()

    st.header("🤖 Industrial AI Assistant")

    st.caption(
        "Ask questions about Equipment Manuals, SOPs, "
        "Maintenance Logs, Inspection Reports, Incident Reports and Regulations."
    )

    with st.expander("💡 Example Questions"):

        st.markdown("""
- How do I start the rotary kiln?
- Explain the startup procedure for the Rotary Kiln.
- What is the use of Bucket Elevator?
- Show maintenance information for BM001.
- Show inspection report for ENG001.
- Explain Ball Mill.
- List incidents related to VRM001.
- Explain the purpose of the Cummins Engine.
""")

    st.divider()

    # ------------------------------------------------------------
    # Session State
    # ------------------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ------------------------------------------------------------
    # Show Previous Conversation
    # ------------------------------------------------------------

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

            if msg["role"] == "assistant":

                if "sources" in msg:

                    with st.expander("📄 Source Documents"):

                        for source, category, chunks in msg["sources"]:

                            icon = get_icon(category)

                            st.write(
                                f"{icon} **{source}** ({category}) • {chunks} chunk(s)"
                            )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Knowledge Sources",
                        msg["source_count"]
                    )

                    col2.metric(
                        "Retrieved Chunks",
                        msg["chunks"]
                    )

                    col3.metric(
                        "Response Time",
                        f"{msg['time']:.2f} sec"
                    )

    # ------------------------------------------------------------
    # User Input
    # ------------------------------------------------------------

    prompt = st.chat_input(
        "Ask something about the cement plant..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Searching industrial knowledge base..."):

                start = time.time()

                try:

                    answer, sources, docs = rag.ask(prompt)

                except Exception as e:

                    st.error(str(e))
                    return

                elapsed = round(time.time() - start, 2)

            st.markdown(answer)

            # --------------------------------------------------------
            # Count Chunks Per Source
            # --------------------------------------------------------

            counter = Counter()

            for doc in docs:
                counter[doc.metadata.get("source")] += 1

            source_info = []

            with st.expander("📄 Source Documents"):

                if len(sources) == 0:

                    st.info("No supporting documents found.")

                else:

                    for source, category in sources:

                        chunks = counter[source]

                        source_info.append(
                            (
                                source,
                                category,
                                chunks
                            )
                        )

                        st.write(
                            f"{get_icon(category)} "
                            f"**{source}** "
                            f"({category}) • "
                            f"{chunks} chunk(s)"
                        )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Knowledge Sources",
                len(sources)
            )

            col2.metric(
                "Retrieved Chunks",
                len(docs)
            )

            col3.metric(
                "Response Time",
                f"{elapsed:.2f} sec"
            )

        # ------------------------------------------------------------
        # Save Assistant Response
        # ------------------------------------------------------------

        st.session_state.messages.append(

            {
                "role": "assistant",

                "content": answer,

                "sources": source_info,

                "source_count": len(sources),

                "chunks": len(docs),

                "time": elapsed

            }

        )