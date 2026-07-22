import streamlit as st
import os
import shutil

from backend.vectorstore import create_vector_database

# -----------------------------
# Category Mapping
# -----------------------------

CATEGORY_PATHS = {
    "Equipment Manual": "data/manuals",
    "SOP Document": "data/sops",
    "Regulation": "data/regulations",
    "Maintenance Log (CSV)": "data/maintenance_logs",
    "Inspection Report (CSV)": "data/inspection_reports",
    "Incident Report (CSV)": "data/incident_reports",
}

# Create folders if they don't exist
for folder in CATEGORY_PATHS.values():
    os.makedirs(folder, exist_ok=True)


# -----------------------------
# Upload Page
# -----------------------------

def show_upload():

    st.title("📂 Industrial Document Upload")

    st.markdown("""
Upload industrial documents to build the AI Knowledge Base.

Supported categories:

- 📘 Equipment Manuals
- 📄 SOP Documents
- 📑 Regulations
- 📊 Maintenance Logs
- 🔍 Inspection Reports
- ⚠ Incident Reports
""")

    st.divider()

    # -----------------------------
    # Category Selection
    # -----------------------------

    category = st.selectbox(
        "Select Document Category",
        list(CATEGORY_PATHS.keys())
    )

    upload_folder = CATEGORY_PATHS[category]

    st.info(f"Files will be stored in **{upload_folder}**")

    # -----------------------------
    # Allowed File Types
    # -----------------------------

    if "CSV" in category:
        allowed = ["csv"]
    else:
        allowed = ["pdf", "docx"]

    uploaded_files = st.file_uploader(
        "Choose Files",
        type=allowed,
        accept_multiple_files=True
    )

    # -----------------------------
    # Upload
    # -----------------------------

    if uploaded_files:

        progress = st.progress(0)

        status = st.empty()

        total = len(uploaded_files)

        for i, file in enumerate(uploaded_files):

            filepath = os.path.join(upload_folder, file.name)

            with open(filepath, "wb") as f:
                f.write(file.getbuffer())

            progress.progress((i + 1) / total)

            status.info(f"Uploading {file.name}")

        status.success("Upload Completed")

        st.success(f"✅ {total} file(s) uploaded successfully.")

        st.divider()

        # -----------------------------
        # Build Vector Database
        # -----------------------------

        with st.spinner("Creating Vector Database..."):

            try:

                create_vector_database()

                st.success("✅ Chroma Vector Database Updated Successfully!")

            except Exception as e:

                st.error(f"Vector Database Error:\n\n{e}")

    # -----------------------------
    # Existing Files
    # -----------------------------

    st.divider()

    st.subheader("📁 Uploaded Files")

    total_files = 0

    for category_name, folder in CATEGORY_PATHS.items():

        files = os.listdir(folder)

        if len(files) == 0:
            continue

        st.markdown(f"### {category_name}")

        for file in files:

            total_files += 1

            filepath = os.path.join(folder, file)

            size = round(os.path.getsize(filepath) / 1024, 2)

            c1, c2, c3 = st.columns([6, 2, 1])

            with c1:
                st.write(f"📄 {file}")

            with c2:
                st.write(f"{size} KB")

            with c3:

                if st.button("🗑", key=f"{folder}_{file}"):

                    os.remove(filepath)

                    st.rerun()

    if total_files == 0:
        st.info("No uploaded files found.")

    # -----------------------------
    # Statistics
    # -----------------------------

    st.divider()

    st.subheader("📊 Dataset Statistics")

    manuals = len(os.listdir("data/manuals"))
    sops = len(os.listdir("data/sops"))
    regulations = len(os.listdir("data/regulations"))
    maintenance = len(os.listdir("data/maintenance_logs"))
    inspection = len(os.listdir("data/inspection_reports"))
    incidents = len(os.listdir("data/incident_reports"))

    c1, c2, c3 = st.columns(3)

    c1.metric("Manuals", manuals)
    c2.metric("SOPs", sops)
    c3.metric("Regulations", regulations)

    c4, c5, c6 = st.columns(3)

    c4.metric("Maintenance Logs", maintenance)
    c5.metric("Inspection Reports", inspection)
    c6.metric("Incident Reports", incidents)

    # # -----------------------------
    # # Clear Database
    # # -----------------------------

    # st.divider()

    # if st.button("🗑 Clear All Uploaded Documents", type="secondary"):

    #     for folder in CATEGORY_PATHS.values():

    #         for file in os.listdir(folder):

    #             os.remove(os.path.join(folder, file))

    #     if os.path.exists("database/chroma_db"):
    #         shutil.rmtree("database/chroma_db")

    #     st.success("All uploaded documents and vector database deleted.")

    #     st.rerun()