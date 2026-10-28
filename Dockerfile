FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m -u 1000 appuser && mkdir -p /app/assets && chown -R appuser:appuser /app
USER appuser
ENV HOME=/home/appuser PYTHONUNBUFFERED=1 PORT=7860
EXPOSE 7860
CMD ["python", "main.py"]

