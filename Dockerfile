FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR $HOME/app

COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY ./ ./

RUN chmod +x ./app-start.sh

EXPOSE 8000
ENTRYPOINT ["./app-start.sh"]


RUN chmod +x ./app-start.sh

