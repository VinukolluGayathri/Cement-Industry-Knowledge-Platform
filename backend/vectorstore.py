import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.loader import IndustrialLoader


load_dotenv()


def create_vector_database():

    print("Loading documents...")

    loader = IndustrialLoader()

    documents = loader.load_documents()

    print(f"Loaded {len(documents)} documents")

    print("Splitting into chunks...")

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=700,
        chunk_overlap=200

    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating Chroma Database...")

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory="database/chroma_db"

    )

    print("=" * 60)
    print("✅ Vector Database Created Successfully!")
    print("=" * 60)

    return db


if __name__ == "__main__":

    create_vector_database()