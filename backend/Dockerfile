FROM python:3.12-slim

# 1. Install system C-libraries
RUN apt-get update && apt-get install -y libpq-dev gcc

# 2. Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /bin/uv

WORKDIR /backend

# 3. Copy ONLY lockfiles first to create a cached dependency layer
COPY pyproject.toml uv.lock ./

# 4. Install dependencies WITHOUT installing the root project
RUN uv sync --frozen --no-cache --no-install-project

# 5. Copy the rest of your application code
COPY . .

# 6. Final fast sync to register your app code
RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]