#!/usr/bin/env bash
# requirements.txt ile bağımlılıkları yükle
pip install -r requirements.txt

# Playwright için Chromium'u indir
playwright install chromium
