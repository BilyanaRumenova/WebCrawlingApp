FROM mcr.microsoft.com/playwright/python:v1.39.0-jammy

COPY . /app
WORKDIR /app

RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
