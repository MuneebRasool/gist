FROM python:3.12-slim


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*


COPY . /app


WORKDIR /app
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir uvicorn aerich


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
