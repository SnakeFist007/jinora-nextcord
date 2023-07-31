FROM python:3.11.4-slim
LABEL org.opencontainers.image.source = "https://github.com/SnakeFist007/jinora-nextcord"

# Add new non-root user
RUN adduser --system --no-create-home jinora

WORKDIR /bot

# Give jinora permissions, otherwise log file creation fails
RUN chown -R jinora /bot \
    && chmod 755 /bot

# Install dependencies
COPY requirements .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /bot/requirements

COPY . .

USER jinora
ENTRYPOINT ["python", "main.py"]
