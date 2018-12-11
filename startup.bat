@echo off
title "payment_in"
set FLASK_APP=payment_in.py
set FLASK_DEBUG=1
flask run --host=127.0.0.1 --port 5004