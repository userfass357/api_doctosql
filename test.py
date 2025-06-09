import requests

url = "http://127.0.0.1:8000/upload/"
file_path = "C:\\Users\\jejax\\Desktop\\api_doctosql\\курсовая Козинский v3.docx"

with open(file_path, "rb") as f:
    files = {"file": (file_path, f, "application/octet-stream")}
    response = requests.post(url, files=files)

print(response.json())