FROM python:3.11.4

WORKDIR /bot

RUN pip uninstall discord.py
RUN pip install nextcord typing requests Pillow pymongo python-dotenv

COPY . .

CMD ["python", "main.py"]