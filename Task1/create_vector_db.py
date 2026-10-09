import sqlite3
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB_FILE = 'profile.db'


def load_documents(db_file=DB_FILE):
    conn = sqlite3.connect(db_file)
    rows = conn.execute('select id, source, title, content from documents').fetchall()
    conn.close()
    documents = []
    for id_, source, title, content in rows:
        documents.append(Document(
            page_content=title + '\n' + content,
            metadata={'id': id_, 'source': source, 'title': title},
        ))
    return documents


def build_vector_db(db_file=DB_FILE):
    document = load_documents(db_file)
    splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_documents(document)
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'},
    )
    vectorDB = FAISS.from_documents(chunks, embeddings)
    return vectorDB, len(document), len(chunks)


if __name__ == '__main__':
    vectorDB, n_docs, n_chunks = build_vector_db()
    print('documents :', n_docs, '| chunks :', n_chunks)

    query = 'where did muhammad work before cellula ?'
    similar_docs = vectorDB.similarity_search_with_score(query, k=3)
    for i in similar_docs:
        print(round(float(i[1]), 3), i[0].metadata['source'], '-', i[0].metadata['title'])
