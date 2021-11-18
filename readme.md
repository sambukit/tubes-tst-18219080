File ini membutuhkan Python 3, FastAPI, PyJWT, dan Uvicorn agar dapat berjalan di perangkat Anda.

Jika Python 3 sudah terinstall, persiapkan virtual environment:
• pipenv install    #install virtual environment
• pipenv shell      #activate virtual env
• exit              #deactivate virtual env

Install FastAPI:
• pip3 install fastapi  #install FastAPI

Install Uvicorn:
• pip3 install uvicorn          #install uvicorn
• uvicorn main:app --reload     #menjalankan uvicorn

Buka IP:port yang disediakan Uvicorn, lalu tambahkan /docs di belakang link untuk mencoba GET, POST, DELETE, UPDATE(PUT)
Misal: http://127.0.0.1:8000/docs

Samuel Aristides
18219080