import streamlit as st
import os

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def show_upload():

    st.header("📂 Upload Industrial Documents")

    st.markdown("""
Upload industrial documents such as:

- 📘 Equipment Manuals
- 📄 SOP Documents
- 📑 Regulations
- 📊 CSV Files
- 🖼 Images
""")

    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "csv", "docx", "xlsx", "png", "jpg"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for file in uploaded_files:

            filepath = os.path.join(UPLOAD_FOLDER, file.name)

            with open(filepath, "wb") as f:
                f.write(file.getbuffer())

        st.success(f"✅ {len(uploaded_files)} files uploaded successfully.")

        st.divider()

        st.subheader("Uploaded Files")

        for file in uploaded_files:
            st.write("📄", file.name)

        st.info("Backend processing (OCR, Chunking, Embeddings) will start automatically once integrated.")