FROM python:3.12-alpine

WORKDIR /app

ARG PORT=3000
ENV PORT=${PORT}

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${PORT}

CMD ["python", "server.py"]