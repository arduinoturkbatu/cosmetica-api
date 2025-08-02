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
wget https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/1276533/chrome-linux.zip
unzip chrome-linux.zip


# Paketleri yükle
npm install

# Puppeteer Chrome'u indir
npx puppeteer browsers install chrome

# testing
npm ls puppeteer-core
