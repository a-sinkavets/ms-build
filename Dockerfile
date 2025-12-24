FROM python:3.11-alpine

LABEL maintainer="github.com/a-sinkavets" \
      description="A Python application that generates errors based on environment variables."

WORKDIR /app

RUN adduser -D -u 1000 appuser && \
    chown appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

ENV PATH=/home/appuser/.local/bin:$PATH

COPY --chown=appuser:appuser src/error_generator.py ./src/

ENTRYPOINT ["python", "-u", "src/error_generator.py"]
