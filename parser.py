from typing import Optional

def parse_document(file_bytes: bytes) -> str:
    # Попробуем обработать .docx
    try:
        from docx import Document
        import io
        file_stream = io.BytesIO(file_bytes)
        doc = Document(file_stream)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    except Exception:
        pass
    # Попробуем декодировать как текстовый файл
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return file_bytes.decode("cp1251")
        except UnicodeDecodeError:
            return "[Ошибка декодирования файла]"