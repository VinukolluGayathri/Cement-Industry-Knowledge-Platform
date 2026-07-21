from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def create_chunks(self, text):

        return self.splitter.create_documents([text])


if __name__ == "__main__":

    from parser import DocumentParser

    parser = DocumentParser()

    text = parser.parse_document("data/manuals/ball_mill.pdf")

    chunker = TextChunker()

    chunks = chunker.create_chunks(text)

    print("=" * 80)
    print(f"Total Chunks : {len(chunks)}")
    print("=" * 80)

    print(chunks[0].page_content)