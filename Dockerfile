FROM python:3.11

RUN apt -y update && apt -y install dnsutils iproute2 iputils-ping

COPY simple_server.py .
COPY serve.sh .

ENV PYTHONUNBUFFERED=1

CMD [ "./serve.sh" ]
