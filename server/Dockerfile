FROM python:3.10.11
WORKDIR /server
COPY . .

ENV ENVIRONMENT=production

RUN python -m pip install -r requirements.txt

EXPOSE 8080 
CMD python main.py