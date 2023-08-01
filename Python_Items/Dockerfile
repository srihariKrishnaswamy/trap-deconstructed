FROM python:3-alpine3.10
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python3 ./server.py