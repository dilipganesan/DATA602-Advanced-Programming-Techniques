FROM python:3.5

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN git clone https://04544f94f4d3bca2e9f803da759b0fe9352fb014@github.com/dilipganesan/DATA602.git

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD [ "python", "traderapp.py" ]
