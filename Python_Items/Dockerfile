FROM --platform=linux/amd64 python:3.10
RUN apt-get update && apt-get install -y libsndfile1
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 3500
CMD ["gunicorn", "--bind", "0.0.0.0:3500", "server:app"]