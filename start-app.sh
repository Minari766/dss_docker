#!/bin/bash

# ①DBサーバ(コンテナ)の起動を待機する
sleep 15

# ②DBのテーブルを作成する（マイグレーション）
python3 manage.py migrate

# ③アプリケーション起動
gunicorn mysite.wsgi:application -b 0:8000

