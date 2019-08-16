FROM python:3.7

RUN mkdir /app
COPY / /app/

RUN cd /app && pip install -r requirements.txt && \
    cd /app/python3-krakenex && pip install --user .

WORKDIR /app
CMD python app.py