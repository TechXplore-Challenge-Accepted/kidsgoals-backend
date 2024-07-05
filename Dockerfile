FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN sudo apt update -y && sudo apt upgrade -y && \
    sudo apt install -y wget build-essential checkinstall  libreadline-gplv2-dev  libncursesw5-dev  libssl-dev  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    cd /usr/src && \
    sudo wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz && \
    sudo tar xzf Python-3.12.4.tgz && \
    cd Python-3.12.4 && \
    sudo ./configure --enable-optimizations && \
    sudo make altinstall
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]