FROM python:3

ENV PYTHONUNBUFFERED = 1
WORKDIR /code
COPY requirements.txt /code/
COPY ./scripts /scripts



RUN pip install -r requirements.txt && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

COPY default.jpeg /code/media/


COPY . /code/
CMD [ "/scripts/run.sh" ]