FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --nocache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "Interface_graphique.py"]