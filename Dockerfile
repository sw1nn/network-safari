FROM python:3.11

RUN apt-get -y update && apt-get -y install dnsutils iproute2 iputils-ping

COPY safari.cert safari.key src/simple_server.py serve.sh ./

ENV PYTHONUNBUFFERED=1

CMD [ "./serve.sh" ]
