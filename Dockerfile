FROM python:3.11-slim

WORKDIR /app
RUN pip install fastapi uvicorn pillow zplgrf python-multipart

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main.py", "--host", "0.0.0.0", "--port", "8000"]