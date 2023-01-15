FROM python:3.11

COPY simple_server.py .
COPY serve.sh .

ENV PYTHONUNBUFFERED=1

CMD [ "./serve.sh" ]
