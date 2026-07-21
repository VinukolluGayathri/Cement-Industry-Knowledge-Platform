import streamlit as st
import networkx as nx
import plotly.graph_objects as go


def show_graph():

    st.header("🕸 Industrial Knowledge Graph")

    st.markdown(
        """
This graph shows relationships between equipment,
manuals, SOPs, maintenance records and regulations.
"""
    )

    G = nx.Graph()

    # Equipment
    G.add_node("BM-101")
    G.add_node("RK-101")
    G.add_node("VRM-101")
    G.add_node("JC-101")
    G.add_node("BC-101")

    # Documents
    G.add_node("Ball Mill Manual")
    G.add_node("Rotary Kiln Manual")
    G.add_node("VRM SOP")
    G.add_node("Maintenance")
    G.add_node("Inspection")
    G.add_node("Regulations")

    # Relationships
    G.add_edge("BM-101", "Ball Mill Manual")
    G.add_edge("BM-101", "Maintenance")
    G.add_edge("BM-101", "Inspection")

    G.add_edge("RK-101", "Rotary Kiln Manual")
    G.add_edge("RK-101", "Maintenance")
    G.add_edge("RK-101", "Regulations")

    G.add_edge("VRM-101", "VRM SOP")
    G.add_edge("VRM-101", "Inspection")

    G.add_edge("JC-101", "Maintenance")

    G.add_edge("BC-101", "Inspection")

    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2),
        hoverinfo="none",
        mode="lines"
    )

    node_x = []
    node_y = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(G.nodes()),
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            size=25
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace]
    )

    fig.update_layout(
        showlegend=False,
        height=650,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)