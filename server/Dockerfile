FROM python:3.11-slim

WORKDIR /app

# system deps for PyMuPDF
RUN apt-get update && apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 poppler-utils && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV CHROMA_PERSIST_DIR=/data/chroma

# create directories
RUN mkdir -p /data/chroma /app/uploaded_files

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
