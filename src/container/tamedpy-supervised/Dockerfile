FROM python:3

RUN ["adduser",  "--home",  "/tmp/sb", "--system", "sandboxuser"]
RUN ["chown", "-R", "sandboxuser", "/tmp/sb"]
RUN ["chmod", "-R", "u+rwx", "/tmp/sb"]

WORKDIR /tmp/sb

COPY ./driver.py /tmp/sb/driver.py
COPY ./requirements.txt /tmp/sb/requirements.txt

RUN ["pip", "install", "-r", "/tmp/sb/requirements.txt"]

CMD [ "python", "driver.py" ]
