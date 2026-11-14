FROM python:3.12-slim
WORKDIR /app
COPY requirements-ai.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY telemetry_simulator.py ./telemetry_simulator.py
EXPOSE 8001
CMD ["uvicorn","app.ai_pipeline:app","--host","0.0.0.0","--port","8001"]
