import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

DOCUMENTS_DIR = Path("documents")
INDEX_DIR = Path("faiss_index")

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError(
        "Chua cau hinh GOOGLE_API_KEY. Hay tao file .env tu .env.example."
    )

# Gemini dung de tao cau tra loi.
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL"),
    temperature=0
)

# Embedding dung de ma hoa cau hoi va cac doan tai lieu.
embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "gemini-embedding-001"),
)


def build_or_load_vectorstore():
    """Nap FAISS neu da co; neu chua co thi doc PDF va tao chi muc moi."""
    if INDEX_DIR.exists():
        print("Dang nap FAISS index da luu...")
        return FAISS.load_local(
            str(INDEX_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            "Khong tim thay PDF. Hay dat it nhat mot file PDF trong thu muc documents."
        )

    documents = []
    for pdf_file in pdf_files:
        print(f"Dang doc: {pdf_file}")
        documents.extend(PyPDFLoader(str(pdf_file)).load())

    if not documents:
        raise ValueError("Khong trich xuat duoc noi dung tu cac file PDF.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Tai lieu khong co noi dung van ban de tao embedding.")

    print(f"Dang tao embedding cho {len(chunks)} doan...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(INDEX_DIR))
    print("Da tao va luu FAISS index.")
    return vectorstore


prompt = ChatPromptTemplate.from_template(
    """Ban la chatbot hoi dap dua tren tai lieu duoc cung cap.

Hay tra loi bang tieng Viet, ro rang va dung trong tam.
Chi dua vao ngu canh ben duoi. Khong tu suy dien thanh su that.
Neu ngu canh khong co thong tin de tra loi, hay noi:
"Toi khong tim thay thong tin nay trong tai lieu."

Ngu canh:
{context}

Cau hoi: {question}
"""
)



def ask_question(vectorstore, question):
    docs = vectorstore.similarity_search(
        question,
        k=4
    )

    if not docs:
        print("\nChatbot: Khong tim thay tai lieu phu hop.")
        return

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    # Chi lay noi dung van ban
    content = response.content

    if isinstance(content, list):
        answer = "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )
    else:
        answer = str(content)

    print("\nChatbot:", answer)

    print("\nNguon tham khao:")
    for doc in docs:
        page = doc.metadata.get("page")
        page_text = page + 1 if isinstance(page, int) else "Khong ro"

        print(
            "- File:", doc.metadata.get("source"),
            "| Trang:", page_text
        )



def main():
    vectorstore = build_or_load_vectorstore()
    print("\nRAG Chatbot da san sang. Nhap 'thoat' de ket thuc.")

    while True:
        question = input("\nBan: ").strip()
        if question.lower() in {"exit", "quit", "thoat"}:
            print("Tam biet!")
            break
        if not question:
            continue

        try:
            ask_question(vectorstore, question)
        except Exception as exc:
            print(f"\nDa xay ra loi khi xu ly cau hoi: {exc}")


if __name__ == "__main__":
    main()
