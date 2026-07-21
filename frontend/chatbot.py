import streamlit as st

def show_chatbot():

    st.header("🤖 Industrial AI Assistant")

    st.markdown(
        """
Ask questions about:

- 📘 Equipment Manuals
- 📄 SOPs
- ⚙ Maintenance Records
- 🔍 Inspection Reports
- ⚠ Incident Reports
- 📑 Regulations
"""
    )

    st.divider()

    question = st.text_input(
        "Ask your question",
        placeholder="Example: Explain the startup procedure for the Rotary Kiln."
    )

    if st.button("Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        with st.spinner("Searching documents..."):

            # Backend will replace this later
            answer = """
This is a placeholder response.

Once the backend RAG pipeline is connected, answers will be generated
from the uploaded manuals, SOPs, maintenance logs and regulations.
"""

            sources = [
                "Rotary_Kiln_Operation_Manual.pdf",
                "Kiln_Startup_SOP.pdf",
                "maintenance_data.csv"
            ]

            confidence = 95

        st.success("Answer")

        st.write(answer)

        st.divider()

        st.subheader("📄 Source Documents")

        for src in sources:
            st.write("✅", src)

        st.divider()

        st.metric("Confidence", f"{confidence}%")