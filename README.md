# Instruktioner för att köra programmet
1. Skapa en ny virtual environment med ```python -m venv .venv```
2. Aktivera virtual environment med ```source .venv/bin/activate```
3. Installera python requirements med  ```pip install -r requirements.txt```
4. Starta flask applikationen med ```flask run```
5. Gå till [http://127.0.0.1:5000](http://127.0.0.1:5000)
6. Gå till [http://127.0.0.1:5000/async-route](http://127.0.0.1:5000/async-route) för en async variant (ingen performance increase för flask är använder endast en worker, kan lösas genom att använda greenlet eller liknande)