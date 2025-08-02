#!/usr/bin/env bash

# Ortamı güncelle
apt-get update

# Gerekirse curl, wget gibi araçları yükle (genelde hazır olur)
apt-get install -y curl

# Sanal ortam oluştur ve aktif et (opsiyonel ama önerilir)
python3 -m venv .venv
source .venv/bin/activate

# pip'i güncelle
pip install --upgrade pip

# Gerekli paketleri yükle
pip install -r requirements.txt

# (Opsiyonel) cache temizle
pip cache purge
