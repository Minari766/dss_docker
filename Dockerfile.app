# Docker Hubからもってくる
FROM python:3.8.3
ENV PYTHONBUFFERED 1

# WORKDIRはDockerfile 内で以降に続く RUN 、 CMD 、 ENTRYPOINT 、 COPY 、 ADD 命令の処理時に（コマンドを実行する場所として）使う 作業ディレクトリ（working directory）を指定
# 今回は/app ディレクトリ内で作業することを指定
WORKDIR /app

# ソースコードを全部配置する
COPY ./ ./

# RUNはコマンド（CMD）を実行
# 今回はPythonライブライリをインストールことを実行
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 manage.py migrate

# gunicornコマンド実行(requirements.txt のライブラリをインストールしたことでコマンドもインストールされる)
# mysiteというディレクトリにあるwsgi.pyファイルのapplication変数をさす
# -b オプション(--bind)おまじない ※localhost(=127.0.0.1) 以外からアクセスを許可するようにする
CMD ["gunicorn", "mysite.wsgi:application", "-b", "0:8000"]

# EXPOSEは無くても動く。メモ的な使い方である
EXPOSE 8000
