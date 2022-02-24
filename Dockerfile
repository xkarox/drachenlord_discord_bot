FROM python:3.10-alpine

RUN pip install -r requirements.txt

CMD ["python", "main.py"]