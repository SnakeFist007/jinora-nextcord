FROM python:3.11.4

WORKDIR /bot

RUN pip uninstall discord.py
RUN pip install -r requirements

COPY . .

CMD ["python", "main.py"]