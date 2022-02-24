FROM python:3.10

COPY . /home/drachenlord

WORKDIR /home/drachenlord

RUN pip install -r requirements.txt

CMD ["python", "main.py"]