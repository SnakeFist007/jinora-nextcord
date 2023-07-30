FROM python:3.11.4
LABEL org.opencontainers.image.source = "https://github.com/SnakeFist007/jinora-nextcord"

COPY requirements /bot/requirements
WORKDIR /bot

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /bot/requirements

COPY . .

CMD ["python", "main.py"]
