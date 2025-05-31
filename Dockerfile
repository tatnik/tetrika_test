FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && pip3 install -r requirements.txt

COPY . ./code

CMD ["python", "main.py"]
