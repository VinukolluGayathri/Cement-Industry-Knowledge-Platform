
# 🏭 Cement Industry Knowledge Platform

An AI-powered Industrial Knowledge Intelligence Platform built using Streamlit, LangChain, ChromaDB, and Google Gemini.

## Features

- Interactive Dashboard
- AI Assistant (RAG)
- Document Upload
- Knowledge Graph
- Chroma Vector Database
- Semantic Search
- PDF, DOCX and CSV Support

## Tech Stack

- Streamlit
- LangChain
- Google Gemini
- ChromaDB
- Hugging Face Embeddings
- NetworkX
- Plotly
- Pandas
- PyPDF
- python-docx

## Project Structure

```text
backend/
frontend/
data/
database/chroma_db/
uploads/
app.py
```

## Installation

```bash
git clone https://github.com/VinukolluGayathri/Cement-Industry-Knowledge-Platform.git
cd Cement-Industry-Knowledge-Platform
python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Run:

```bash
streamlit run app.py
```

## Modules

### Dashboard
Displays industrial KPIs and project overview.

### Upload
Uploads manuals, SOPs, regulations, maintenance logs, inspection reports and automatically rebuilds the Chroma vector database.

### AI Assistant
Uses Retrieval-Augmented Generation (RAG):

User Query → ChromaDB → Relevant Chunks → Gemini → Response

### Knowledge Graph
Visualizes relationships among equipment, manuals, SOPs, maintenance, inspections and regulations using NetworkX and Plotly.

## Dataset

- Manuals (PDF)
- SOPs (PDF/DOCX)
- Regulations (PDF)
- Maintenance Logs (CSV)
- Inspection Reports (CSV)
- Incident Reports (CSV)

## Future Enhancements

- OCR
- Voice Assistant
- Predictive Maintenance
- Neo4j Integration
- Real-time IoT Support

## Contributors

- Vinukollu Gayathri
- Potluri Supraja

## License

Educational and Hackathon Project.
