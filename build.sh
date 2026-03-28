#!/usr/bin/env bash
set -e

pip install -r requirements.txt

# Install Chromium + ChromeDriver (required for Selenium on Render)
apt-get update -y
apt-get install -y chromium chromium-driver

echo "Build complete."
