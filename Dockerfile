FROM python:3.11.4

COPY requirements /bot/requirements
WORKDIR /bot

RUN pip install --upgrade pip
RUN pip install -r /bot/requirements

COPY . .

CMD ["python", "main.py"]