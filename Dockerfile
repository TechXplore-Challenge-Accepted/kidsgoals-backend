FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt


RUN sudo wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz
RUN sudo tar xzf Python-3.12.4.tgz
RUN cd Python-3.12.4
RUN sudo ./configure --enable-optimizations
RUN sudo make install
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]