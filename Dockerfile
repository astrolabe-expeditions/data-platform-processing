FROM python:3.11-slim
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -qr requirements.txt
COPY ./src .

CMD ["python3", "./sqs.py"]