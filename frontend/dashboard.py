import streamlit as st
import pandas as pd
import os

def show_dashboard():

    st.header("📊 Cement Factory Dashboard")
    st.markdown("### AI-Powered Industrial Knowledge Intelligence Platform")

    DATA_PATH = "data"

    manual_count = len(os.listdir(os.path.join(DATA_PATH, "manuals")))
    sop_count = len(os.listdir(os.path.join(DATA_PATH, "sops")))
    regulation_count = len(os.listdir(os.path.join(DATA_PATH, "regulations")))

    maintenance = pd.read_csv(
        os.path.join(DATA_PATH, "maintenance_logs", "maintenance_data.csv")
    )

    inspection = pd.read_csv(
        os.path.join(DATA_PATH, "inspection_reports", "inspection_data.csv")
    )

    incident = pd.read_csv(
        os.path.join(DATA_PATH, "incident_reports", "incident_data.csv")
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📘 Manuals", manual_count)

    with col2:
        st.metric("📄 SOPs", sop_count)

    with col3:
        st.metric("📑 Regulations", regulation_count)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("🛠 Maintenance Records", len(maintenance))

    with col5:
        st.metric("🔍 Inspection Reports", len(inspection))

    with col6:
        st.metric("⚠ Incident Reports", len(incident))

    st.divider()

    st.subheader("🏭 Plant Equipment")

    equipment = [
        "BM-101 Ball Mill",
        "VRM-101 Vertical Roller Mill",
        "RK-101 Rotary Kiln",
        "JC-101 Jaw Crusher",
        "BC-101 Belt Conveyor",
        "BE-101 Bucket Elevator",
        "BF-101 Bag Filter",
        "AC-101 Air Compressor",
        "P-101 Centrifugal Pump",
        "GB-101 Gearbox",
        "CE-101 Cummins Engine"
    ]

    c1, c2, c3 = st.columns(3)

    for i, eq in enumerate(equipment):

        if i % 3 == 0:
            c1.success(eq)

        elif i % 3 == 1:
            c2.info(eq)

        else:
            c3.warning(eq)

    st.divider()

    st.subheader("📂 Dataset Summary")

    summary = pd.DataFrame({

        "Dataset": [
            "Equipment Manuals",
            "SOP Documents",
            "Regulations",
            "Maintenance Logs",
            "Inspection Reports",
            "Incident Reports"
        ],

        "Count": [
            manual_count,
            sop_count,
            regulation_count,
            len(maintenance),
            len(inspection),
            len(incident)
        ]

    })

    st.dataframe(summary, use_container_width=True)