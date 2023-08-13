FROM python:3.9-slim

RUN apt update && apt install nginx -y

COPY  ./nginx/default.conf /etc/nginx/conf.d/default.conf

COPY . .

RUN pip install -r requirements.txt

WORKDIR /another_social_app
COPY run.sh .

RUN chmod +x run.sh

CMD [ "./run.sh" ]