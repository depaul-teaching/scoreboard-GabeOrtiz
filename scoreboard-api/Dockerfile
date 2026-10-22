FROM python:3.12-slim
# The pipeline passes the commit SHA in; local builds fall back to local-dev
ARG BUILD_SHA=local-dev
ENV BUILD_SHA=${BUILD_SHA} \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1
WORKDIR /app
# Dependencies first, so this layer stays cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
# Do not run as root
RUN useradd --create-home --uid 10001 appuser
USER 10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]