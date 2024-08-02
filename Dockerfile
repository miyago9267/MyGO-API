FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y curl gcc build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ~/.local/bin/poetry export -f requirements.txt --output requirements.txt

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc build-essential
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "mygo/app.py"]