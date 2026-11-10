# RAG Chatbot - LangChain + Gemini + FAISS

Du an demo RAG chatbot chay local tren Windows, su dung PDF lam nguon tri thuc.

## 1. Yeu cau

- Python 3.10+ (khuyen nghi Python 3.11)
- Google AI Studio API key
- Ket noi Internet khi cai thu vien va goi Gemini API

## 2. Cai dat tren Windows

Mo CMD tai thu muc du an:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Neu dung PowerShell va khong kich hoat duoc venv, co the chay:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Cau hinh API key

1. Tao API key tai https://aistudio.google.com/app/apikey
2. Sao chep `.env.example` thanh `.env`.
3. Dien API key vao `GOOGLE_API_KEY`.

Khong chia se API key va khong commit file `.env` len GitHub.

## 4. Them tai lieu

Dat cac file PDF vao thu muc `documents/`.

Ban demo nay doc cac file PDF o lan chay dau tien va luu vector vao `faiss_index/`.
Neu them, xoa hoac sua tai lieu, hay xoa thu muc `faiss_index/` de tao lai chi muc.

Luu y: tai lieu PDF scan anh co the khong trich xuat duoc van ban neu chua co OCR.

## 5. Chay chatbot

```bat
python main.py
```

Nhap cau hoi bang tieng Viet. Nhap `thoat` de dung chuong trinh.

## 6. RAG hoat dong nhu the nao?

1. PyPDFLoader doc noi dung PDF.
2. RecursiveCharacterTextSplitter chia tai lieu thanh cac chunk.
3. GoogleGenerativeAIEmbeddings tao vector embedding.
4. FAISS luu va tim cac chunk gan voi cau hoi.
5. Gemini nhan ngu canh tim duoc va tao cau tra loi.
6. Chuong trinh hien thi nguon va so trang tham khao.

## 7. Chi phi va bao mat

- LangChain, FAISS va cac thu vien Python trong du an la phan mem co the dung mien phi.
- Gemini API co the co han muc mien phi; quota, model va gia co the thay doi. Kiem tra:
  https://ai.google.dev/gemini-api/docs/pricing
- Qua trinh tao embedding va hoi dap gui du lieu den Google API.
- Khong dua tai lieu nhay cam hoac thong tin ca nhan len API neu chua danh gia chinh sach du lieu.
- Chi nap thu muc `faiss_index/` do chinh ban tao va tin cay, vi FAISS local duoc nap voi co che deserialization.

## 8. Loi thuong gap

- `GOOGLE_API_KEY`: kiem tra file `.env` va ten bien.
- Model khong kha dung: thay `GEMINI_MODEL` bang model Flash dang duoc ho tro tren Google AI Studio.
- Het quota / rate limit: doi quota reset hoac kiem tra han muc tai khoan.
- Khong tim thay PDF: kiem tra file nam truc tiep trong `documents/`, khong phai thu muc con.
- Them tai lieu moi nhung chatbot khong tim thay: xoa `faiss_index/` va chay lai.
