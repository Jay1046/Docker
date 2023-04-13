FROM python:3.9
LABEL version="1.0.0"
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
WORKDIR /data/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["python", "./main.py"]
