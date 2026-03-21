FROM python:3.12-alpine3.22

COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /uvx /bin/

WORKDIR /app

COPY api/requirements.txt .
COPY api/uv.lock .
COPY api/pyproject.toml .

RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    libstdc++

RUN uv sync --frozen --no-dev

COPY api/main.py .
COPY api/ .

CMD ["uv", "run", "python", "main.py"]
