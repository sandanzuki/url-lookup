FROM python:2.7         
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "lookup.py"]
