FROM python:3.11-slim

WORKDIR /app

COPY ./app ./app
COPY ./ui ./ui
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
EXPOSE 8501

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]