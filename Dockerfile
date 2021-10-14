# FROM：dockerhubから持ってくる
FROM python:3.8.3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip3 install -r requirements.txt

ADD . /code/
EXPOSE 8000

COPY ./command.sh /command.sh
CMD ["/command.sh"]
