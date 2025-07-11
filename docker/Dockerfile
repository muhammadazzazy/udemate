FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV CHROMEDRIVER_VERSION=138.0.7204.49

WORKDIR /udemate

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    unzip \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgtk-3-0 \
    libgbm1 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    libxi6 \
    software-properties-common && \
    curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main" \
    | tee /etc/apt/sources.list.d/brave-browser-release.list && \
    apt-get update && \
    apt-get install -y brave-browser && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.49/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    cd chromedriver-linux64 && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    cd .. && \
    rm chromedriver-linux64.zip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip

COPY . .

CMD ["python3", "src/main.py", "--mode", "headless"]

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID usergroup && \
    adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

USER user
