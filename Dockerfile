FROM python:3.12-slim AS builder
WORKDIR /tytti-starter
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"
WORKDIR /episend
RUN useradd --create-home --uid 10001 episend \
    && mkdir -p /home/episend/.local/share/argos-translate \
       /home/episend/.cache/argos-translate \
       /episend/data \
    && chown -R episend:episend /home/episend /episend
COPY --from=builder /opt/venv /opt/venv
COPY --chown=episend:episend . . 
USER episend
CMD ["python", "main.py"]