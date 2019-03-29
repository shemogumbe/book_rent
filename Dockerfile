FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR $HOME/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8000
COPY ./ ./
RUN python manage.py migrate
RUN python manage.py runserver 0.0.0.0:8000