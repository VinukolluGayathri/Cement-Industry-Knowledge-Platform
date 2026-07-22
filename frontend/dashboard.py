import os
import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

DATA_PATH = "data"


# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

@st.cache_data
def load_data():

    maintenance = pd.read_csv(
        os.path.join(DATA_PATH, "maintenance_logs", "maintenance_data.csv")
    )

    inspection = pd.read_csv(
        os.path.join(DATA_PATH, "inspection_reports", "inspection_data.csv")
    )

    incident = pd.read_csv(
        os.path.join(DATA_PATH, "incident_reports", "incident_data.csv")
    )

    return maintenance, inspection, incident


# ----------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------

def load_css():

    st.markdown("""
<style>

/* Main page */
.block-container{
    padding-top:3rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:2rem;
}

/* Hero */
.hero{
    background:linear-gradient(135deg,#172554,#1E293B);
    padding:35px;
    border-radius:18px;
    margin-top:10px;
    margin-bottom:30px;
}

.hero h1{
    font-size:42px;
    margin:0;
    padding-bottom:8px;
    line-height:1.3;
}

.hero p{
    font-size:18px;
    color:#d1d5db;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# MAIN PAGE
# ----------------------------------------------------------

def show_dashboard():

    load_css()

    maintenance, inspection, incident = load_data()

    manual_count = len(os.listdir(os.path.join(DATA_PATH, "manuals")))
    sop_count = len(os.listdir(os.path.join(DATA_PATH, "sops")))
    regulation_count = len(os.listdir(os.path.join(DATA_PATH, "regulations")))

    # ------------------------------------------------------
    # HERO
    # ------------------------------------------------------

    st.markdown("""

    <div class="hero">

    <h1>🏭 Industrial Knowledge Intelligence Platform</h1>

    <p>
    AI-powered decision support system for Cement Manufacturing.
    Retrieve manuals, SOPs, maintenance logs, inspections,
    incidents and regulations in seconds.
    </p>

    </div>

    """, unsafe_allow_html=True)

    # ------------------------------------------------------
    # KPI
    # ------------------------------------------------------

    st.subheader("📊 Knowledge Base Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("📘 Manuals", manual_count)
    c2.metric("📄 SOPs", sop_count)
    c3.metric("📑 Regulations", regulation_count)

    c4, c5, c6 = st.columns(3)

    c4.metric("⚙ Maintenance", len(maintenance))
    c5.metric("🔍 Inspections", len(inspection))
    c6.metric("⚠ Incidents", len(incident))

    st.divider()

    # ------------------------------------------------------
    # EQUIPMENT
    # ------------------------------------------------------

    st.subheader("🏭 Plant Equipment")

    st.markdown("""
    <style>

    .eq-card-green{
        background:#184d2d;
        color:white;
        padding:14px 18px;
        border-radius:10px;
        margin-bottom:12px;
        font-weight:600;
        border-left:5px solid #4ade80;
        font-size:16px;
    }

    .eq-card-blue{
        background:#1e3a8a;
        color:white;
        padding:14px 18px;
        border-radius:10px;
        margin-bottom:12px;
        font-weight:600;
        border-left:5px solid #60a5fa;
        font-size:16px;
    }

    .eq-card-yellow{
        background:#8a6a08;
        color:white;
        padding:14px 18px;
        border-radius:10px;
        margin-bottom:12px;
        font-weight:600;
        border-left:5px solid #facc15;
        font-size:16px;
    }

    </style>
    """, unsafe_allow_html=True)


    green = [
        ("AC-101", "Air Compressor"),
        ("BC-101", "Belt Conveyor"),
        ("CE-101", "Cummins Engine"),
        ("VRM-101", "Vertical Roller Mill")
    ]

    blue = [
        ("BF-101", "Bag Filter"),
        ("BE-101", "Bucket Elevator"),
        ("JC-101", "Jaw Crusher"),
        ("GB-101", "Gearbox")
    ]

    yellow = [
        ("BM-101", "Ball Mill"),
        ("P-101", "Centrifugal Pump"),
        ("RK-101", "Rotary Kiln")
    ]


    col1, col2, col3 = st.columns(3)

    with col1:
        for eid, name in green:
            st.markdown(
                f"""
                <div class="eq-card-green">
                    <b>{eid}</b><br>
                    {name}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        for eid, name in blue:
            st.markdown(
                f"""
                <div class="eq-card-blue">
                    <b>{eid}</b><br>
                    {name}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        for eid, name in yellow:
            st.markdown(
                f"""
                <div class="eq-card-yellow">
                    <b>{eid}</b><br>
                    {name}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()
    # ------------------------------------------------------
    # DATASET DISTRIBUTION
    # ------------------------------------------------------

    st.subheader("📂 Dataset Distribution")

    dataset = pd.DataFrame({

        "Dataset":[
            "Manuals",
            "SOPs",
            "Regulations",
            "Maintenance",
            "Inspection",
            "Incident"
        ],

        "Count":[
            manual_count,
            sop_count,
            regulation_count,
            len(maintenance),
            len(inspection),
            len(incident)
        ]

    })

    left,right = st.columns([1,1])

    with left:

        fig = px.pie(

            dataset,

            names="Dataset",

            values="Count",

            hole=0.55,

            title="Knowledge Base Distribution"

        )

        fig.update_layout(height=420)

        st.plotly_chart(fig,use_container_width=True)

    with right:

        st.dataframe(

            dataset,

            use_container_width=True,

            hide_index=True

        )

    st.divider()

    # ------------------------------------------------------
    # MAINTENANCE ANALYTICS
    # ------------------------------------------------------

    st.subheader("⚙ Maintenance Analytics")

    c1,c2 = st.columns(2)

    with c1:

        type_count = (
            maintenance["MaintenanceType"]
            .value_counts()
            .reset_index()
        )

        type_count.columns=["Type","Count"]

        fig = px.bar(

            type_count,

            x="Type",

            y="Count",

            text="Count",

            title="Maintenance Types"

        )

        fig.update_layout(height=420)

        st.plotly_chart(fig,use_container_width=True)

    with c2:

        priority = (

            maintenance["Priority"]

            .value_counts()

            .reset_index()

        )

        priority.columns=["Priority","Count"]

        fig = px.pie(

            priority,

            names="Priority",

            values="Count",

            hole=0.45,

            title="Maintenance Priority"

        )

        fig.update_layout(height=420)

        st.plotly_chart(fig,use_container_width=True)

    st.divider()

    # ------------------------------------------------------
    # PART 2 STARTS HERE
    # ------------------------------------------------------

   

        # ------------------------------------------------------
    # INSPECTION ANALYTICS
    # ------------------------------------------------------

    st.subheader("🔍 Inspection Analytics")

    col1, col2 = st.columns(2)

    with col1:

        result_df = (
            inspection["Result"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        result_df.columns = ["Result", "Count"]

        fig = px.bar(
            result_df,
            x="Result",
            y="Count",
            text="Count",
            title="Inspection Results"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        type_df = (
            inspection["InspectionType"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        type_df.columns = ["Inspection Type", "Count"]

        fig = px.pie(
            type_df,
            names="Inspection Type",
            values="Count",
            hole=0.45,
            title="Inspection Type Distribution"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ------------------------------------------------------
    # INCIDENT ANALYTICS
    # ------------------------------------------------------

    st.subheader("⚠ Incident Analytics")

    col1, col2 = st.columns(2)

    with col1:

        sev = (
            incident["Severity"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        sev.columns = ["Severity", "Count"]

        fig = px.bar(
            sev,
            x="Severity",
            y="Count",
            color="Severity",
            text="Count",
            title="Incident Severity"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        cat = (
            incident["Category"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        cat.columns = ["Category", "Count"]

        fig = px.pie(
            cat,
            names="Category",
            values="Count",
            hole=0.45,
            title="Incident Categories"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ------------------------------------------------------
    # EQUIPMENT ANALYTICS
    # ------------------------------------------------------

    st.subheader("🏭 Equipment Analytics")

    eq_count = (
        maintenance["EquipmentName"]
        .value_counts()
        .reset_index()
    )

    eq_count.columns = ["Equipment", "Maintenance Records"]

    fig = px.bar(
        eq_count,
        x="Equipment",
        y="Maintenance Records",
        color="Maintenance Records",
        text="Maintenance Records",
        title="Maintenance Records per Equipment"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ------------------------------------------------------
    # DOWNTIME & COST
    # ------------------------------------------------------

    st.subheader("💰 Maintenance Cost & Downtime")

    left, right = st.columns(2)

    with left:

        downtime = (
            maintenance.groupby("EquipmentName")["Downtime_Hours"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            downtime,
            x="EquipmentName",
            y="Downtime_Hours",
            color="Downtime_Hours",
            title="Total Downtime (Hours)"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    with right:

        cost = (
            maintenance.groupby("EquipmentName")["Cost_INR"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            cost,
            x="EquipmentName",
            y="Cost_INR",
            color="Cost_INR",
            title="Maintenance Cost (INR)"
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ------------------------------------------------------
    # RECENT RECORDS
    # ------------------------------------------------------

    st.subheader("📋 Recent Records")

    tab1, tab2, tab3 = st.tabs([
        "Maintenance",
        "Inspection",
        "Incident"
    ])

    with tab1:

        st.dataframe(
            maintenance.sort_values(
                "MaintenanceDate",
                ascending=False
            ).head(10),
            use_container_width=True,
            hide_index=True
        )

    with tab2:

        st.dataframe(
            inspection.sort_values(
                "InspectionDate",
                ascending=False
            ).head(10),
            use_container_width=True,
            hide_index=True
        )

    with tab3:

        st.dataframe(
            incident.sort_values(
                "IncidentDate",
                ascending=False
            ).head(10),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ------------------------------------------------------
    # PLANT HEALTH
    # ------------------------------------------------------

    st.subheader("🟢 Plant Health Overview")

    m_status = maintenance["Status"].astype(str).str.lower()
    i_status = inspection["Status"].astype(str).str.lower()
    inc_status = incident["Status"].astype(str).str.lower()

    completed = m_status.str.contains("complete").sum()
    open_jobs = len(maintenance) - completed

    passed = (
        inspection["Result"]
        .astype(str)
        .str.lower()
        .str.contains("pass")
        .sum()
    )

    critical = (
        incident["Severity"]
        .astype(str)
        .str.lower()
        .str.contains("critical")
        .sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("✅ Completed Jobs", completed)

    c2.metric("🛠 Open Jobs", open_jobs)

    c3.metric("✔ Passed Inspections", passed)

    c4.metric("🚨 Critical Incidents", critical)

    st.divider()

    # ------------------------------------------------------
    # SYSTEM STATUS
    # ------------------------------------------------------

    st.subheader("🤖 AI Platform Status")

    left, right = st.columns(2)

    with left:

        st.success("🟢 Knowledge Base Loaded")
        st.success("🟢 ChromaDB Connected")
        st.success("🟢 Embeddings Ready")
        st.success("🟢 Streamlit Running")

    with right:

        st.info(f"📘 Manuals : {manual_count}")
        st.info(f"📄 SOPs : {sop_count}")
        st.info(f"📑 Regulations : {regulation_count}")
        st.info(f"📂 Total Records : {len(maintenance)+len(inspection)+len(incident)}")

    st.divider()

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------

    st.markdown(
        """
        <center>

        <h4>🏭 Industrial Knowledge Intelligence Platform</h4>

        <p>
        AI-Powered Retrieval Augmented Generation (RAG) System for Cement Industry
        </p>

        <p>
        ET AI Hackathon 2026
        </p>

        </center>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------

if __name__ == "__main__":
    show_dashboard()