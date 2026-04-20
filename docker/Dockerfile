FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

ARG APP_VER=1.0
ENV APP_VERSION=$APP_VER

EXPOSE 5000

CMD ["python", "app.py"]