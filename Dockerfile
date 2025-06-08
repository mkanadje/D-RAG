FROM python:3.11-slim

WORKDIR /app

COPY ./app ./app
COPY ./requirements.txt .
COPY start.sh .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /start.sh

EXPOSE 8080
EXPOSE 8501


CMD ["/start.sh"]