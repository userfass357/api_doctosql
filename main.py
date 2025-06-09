from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
import models
import database
import parser
from urllib.parse import quote

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    content = parser.parse_document(file_bytes)
    doc = models.Document(filename=file.filename, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "filename": doc.filename}

@app.get("/documents/")
def get_documents(db: Session = Depends(get_db)):
    docs = db.query(models.Document).all()
    return [
        {"id": doc.id, "filename": doc.filename, "content": doc.content}
        for doc in docs
    ]

@app.get("/")
def download_document(id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == id).first()
    if not doc:
        return {"error": "Документ не найден"}
    file_content = f"{doc.filename}\n\n{doc.content}"
    file_stream = io.BytesIO(file_content.encode("utf-8"))
    safe_filename = "document.txt"
    quoted_filename = quote(f"{doc.filename}.txt")
    return StreamingResponse(
        file_stream,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={safe_filename}; filename*=UTF-8''{quoted_filename}"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)