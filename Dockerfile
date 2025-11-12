FROM python:3.11-slim

WORKDIR /app

# Copy backend
COPY backend/ ./backend
WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend
WORKDIR /app
COPY frontend/ ./frontend

# Expose Render's port (Render sets PORT env automatically)
EXPOSE 8000

CMD ["python", "backend/app.py"]
