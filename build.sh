#!/usr/bin/env bash

# Cache temizle
rm -rf node_modules package-lock.json
npm cache clean --force

# Sistem paketleri
apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils

# Chromium indir ve aç
mkdir -p /opt/chromium
cd /opt/chromium
wget https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1249841%2Fchrome-linux.zip
unzip chrome-linux.zip


# Paketleri yükle
npm install

# Puppeteer Chrome'u indir
npx puppeteer browsers install chrome

# testing
npm ls puppeteer-core
