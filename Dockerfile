# Build stage
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m pytest --cov=app tests/ --cov-report=xml

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=build /app/app ./app
COPY --from=build /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add non-root user
RUN addgroup --system --gid 1001 appuser && \
    adduser --system --uid 1001 --gid 1001 appuser
USER appuser

EXPOSE 3002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3002"]