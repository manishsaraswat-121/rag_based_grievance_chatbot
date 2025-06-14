FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN python vectordb/prepare_vectors.py
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]