FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install -v requirements.txt --no-cache-dir

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
