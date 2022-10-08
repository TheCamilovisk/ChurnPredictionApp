FROM python:3.9-slim

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

WORKDIR /app
COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["sh", "-c", "python download_model.py && uvicorn churn_api:app --host 0.0.0.0 --port 8000"]