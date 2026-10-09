FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml ./
COPY src ./src
COPY manage.py ./
COPY templates ./templates
COPY static ./static
COPY infra ./infra
RUN python -m pip install --upgrade pip && pip install .
RUN chmod +x /app/infra/docker/entrypoint.sh /app/infra/docker/healthcheck.sh
EXPOSE 8000
ENTRYPOINT ["/app/infra/docker/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
