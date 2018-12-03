FROM python:3

# Define the variables available.
ARG sb_uid
ARG sb_gid

# RUN ["addgroup", "sandboxuser"]
RUN ["adduser",  "--home",  "/tmp/sb", "sandboxuser"]
#RUN ["adduser",  "--home",  "/tmp/sb", "sandboxuser"]
RUN ["chown", "-R", "sandboxuser", "/tmp/sb"]
RUN ["chmod", "-R", "u+rwx", "/tmp/sb"]

WORKDIR /tmp/sb

COPY ./driver.py /tmp/sb/driver.py
COPY ./requirements.txt /tmp/sb/requirements.txt

COPY setup_uid_gid.sh /
# Launch setup.sh
RUN bash /setup_uid_gid.sh "${sb_uid}" "${sb_gid}"

RUN ["pip", "install", "-r", "/tmp/sb/requirements.txt"]

CMD [ "python", "driver.py" ]
