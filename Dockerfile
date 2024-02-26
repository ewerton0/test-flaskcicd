FROM python:3.10-slim

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get install tesseract-ocr-por \
  && python -m pip install -r requirements.txt \
  && apt-get update && apt-get install ffmpeg libsm6 libxext6  -y \
  && apt-get install -y poppler-utils

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]