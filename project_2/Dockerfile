FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ../../../Downloads/kakaochattest_guide-main .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
