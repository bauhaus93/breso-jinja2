#!/bin/sh

rm -f /tmp/breso.sock
source venv/bin/activate
python3 src/main.py
rm -f /tmp/breso.sock
