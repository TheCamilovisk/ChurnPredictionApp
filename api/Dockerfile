FROM python:3.9-slim

COPY Pipfile Pipfile.lock ./
RUN apt update && apt install -y awscli jq
RUN pip install pipenv && pipenv install --system --deploy

WORKDIR /app
COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["sh", "setup-env.sh"]