FROM python:3.5
ADD . /trader
WORKDIR /trader

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "app.py"]