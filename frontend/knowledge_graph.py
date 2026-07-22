import streamlit as st
import networkx as nx
import plotly.graph_objects as go

NODE_COLORS={"Equipment":"#22c55e","Manual":"#3b82f6","SOP":"#facc15","Maintenance":"#f97316","Inspection":"#a855f7","Regulation":"#ef4444"}

def add_nodes(G):
    equipment=[("BM-101","Ball Mill"),("RK-101","Rotary Kiln"),("VRM-101","Vertical Roller Mill"),("JC-101","Jaw Crusher"),("BC-101","Belt Conveyor"),("BE-101","Bucket Elevator"),("BF-101","Bag Filter"),("CE-101","Cummins Engine"),("AC-101","Air Compressor"),("P-101","Centrifugal Pump"),("GB-101","Gearbox")]
    for eid,name in equipment:G.add_node(f"{eid}\n{name}",kind="Equipment")
    manuals=["Ball Mill Manual","Rotary Kiln Manual","VRM Manual","Jaw Crusher Manual","Belt Conveyor Manual","Bucket Elevator Manual","Bag Filter Manual","Cummins Engine Manual","Air Compressor Manual","Pump Manual","Gearbox Manual"]
    for m in manuals:G.add_node(m,kind="Manual")
    sops=["Ball Mill SOP","Rotary Kiln SOP","VRM SOP","Jaw Crusher SOP","Air Compressor SOP","Gearbox SOP"]
    for s in sops:G.add_node(s,kind="SOP")
    for n,k in [("Maintenance Records","Maintenance"),("Inspection Reports","Inspection"),("Plant Regulations","Regulation")]:G.add_node(n,kind=k)
    for eid,name in equipment:
        lbl=f"{eid}\n{name}"
        for m in manuals:
            if name.split()[0] in m:G.add_edge(lbl,m)
        for s in sops:
            if name.split()[0] in s:G.add_edge(lbl,s)
        G.add_edge(lbl,"Maintenance Records");G.add_edge(lbl,"Inspection Reports")
    G.add_edge("RK-101\nRotary Kiln","Plant Regulations");G.add_edge("BM-101\nBall Mill","Plant Regulations")

def show_graph():
    st.markdown("<h1>🕸 Industrial Knowledge Graph</h1>",unsafe_allow_html=True)
    G=nx.Graph();add_nodes(G)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Nodes",len(G.nodes));c2.metric("Edges",len(G.edges));c3.metric("Equipment",11);c4.metric("Documents",len(G.nodes)-11)
    pos=nx.spring_layout(G,seed=42,k=1.2)
    ex=[];ey=[]
    for a,b in G.edges():
        x0,y0=pos[a];x1,y1=pos[b];ex.extend([x0,x1,None]);ey.extend([y0,y1,None])
    traces=[go.Scatter(x=ex,y=ey,mode="lines",line=dict(color="#94a3b8",width=1.5),hoverinfo="none")]
    for kind,color in NODE_COLORS.items():
        xs=[];ys=[];txt=[]
        for n in G.nodes():
            if G.nodes[n]["kind"]==kind:
                x,y=pos[n];xs.append(x);ys.append(y);txt.append(n)
        traces.append(go.Scatter(x=xs,y=ys,mode="markers+text",text=txt,textposition="top center",name=kind,marker=dict(size=24,color=color,line=dict(color="white",width=2))))
    fig=go.Figure(traces)
    fig.update_layout(template="plotly_dark",height=720,xaxis=dict(visible=False),yaxis=dict(visible=False),margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig,use_container_width=True)

if __name__=="__main__":
    show_graph()
