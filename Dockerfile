FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE = 1\
    PYTHONUNBUFFERED = 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

RUN pip install --upgrade --force-reinstall scikit-learn==1.5.2 imbalanced-learn==0.12.4
RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]