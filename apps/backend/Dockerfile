FROM python:3.12-slim

WORKDIR /app

COPY packages/bazi-engine /app/packages/bazi-engine
RUN pip install --no-cache-dir /app/packages/bazi-engine && \
    pip install --no-cache-dir fastapi uvicorn pydantic-settings

COPY apps/backend /app/apps/backend
RUN pip install --no-cache-dir /app/apps/backend

EXPOSE 8000

CMD ["uvicorn", "bazi_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
