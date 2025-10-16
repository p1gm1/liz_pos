FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates \
    build-essential \
    python3-dev \
    python3-setuptools \
    libgl1 \
    make \
    gcc \
    nano \
    net-tools \
    curl

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY . /app

RUN uv venv

RUN uv pip install -r pyproject.toml

CMD ["uv", "run", "streamlit", "run", "src/main.py"]
