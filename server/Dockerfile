FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install wget for healthchecks
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir uvicorn aerich

RUN aerich migrate
RUN aerich upgrade

EXPOSE 8000
# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
