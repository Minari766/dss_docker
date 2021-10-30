- Djangoアプリをコンテナ化する
- コンテナ間を連携する
  - Webサーバ(nginx)もコンテナ化
- ★2021/10/14 done
- docker-compose を使ってコンテナ間を連携する
- EC2上で(sqlite3を使って)アプリケーションを実行する
  - EC2インスタンスをUbuntuで作り直す(今はAmazon Linux2)
- データベースをMySQLにする
  - まずはDBコンテナを手動で起動して、連携する
    - MySQLのバージョンは8.0.26(Tags で最新のバージョンを使う)
    - ユーザ名: `user` => 環境変数`MYSQL_USER`
    - パスワード: `password` => 環境変数`MYSQL_PASSWORD`
    - データベース名: `django_docker` => 環境変数`MYSQL_DATABASE`
    - ※オプションで必要なもの: `MYSQL_ROOT_PASSWORD=password`
    - ⇒起動コマンドは「`docker run -e MYSQL_USER=user -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=django_docker ...`」
  - ★2021/10/19 MySQL & Djangoの相性が悪いため DB にPostgreSQL を使う
    - バージョン: 14.0
    - 環境変数たち
      - `POSTGRES_USER`
      - `POSTGRES_PASSWORD`
      - `POSTGRES_DB`
      - 起動コマンド⇒`docker run -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=django_docker ...`
  - docker-compose で一括起動させる


# 2021/10/23 トラブルシュート対応

## ①AssertionErrorの解決

Webサイト上で会員登録ボタンを押した際に「AssertionError at / database connection isn't set to UTC」が発生しました。
調べたところDjango2.2でpsycopg2のバージョンが2.9を超えると上記エラーが発生するとのことでしたので、

```shell
ubuntu@ip-172-31-38-33:~/dss_docker$ pip install -U psycopg2-2.8.6
```

コマンドでpycong2-binaryのバージョンを2.8.6に変更したものの、同様のエラーが発生してしまいます。

## ②SuperUserの設定

```shell
ubuntu@ip-172-31-38-33:~/dss_docker$ python3 manage.py createsuperuser
...
ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?
```

コマンドでSuperUserの設定を行おうとしたのですが、ImportErrorが発生してしまいます。
Djangoが含まれていないことが原因かと考え、Dockerにインストールされているソフトウェア一覧を確認したところ確かにDjangoが含まれておりませんでした。
requirements.txtにはDjango==2.2.10と記載があるにも関わらず、何故こうなるのでしょうか。


## 解決編

> ubuntu@ip-172-31-38-33:~/dss_docker$ pip install -U psycopg2-2.8.6
> コマンドでpycopg2-binaryのバージョンを2.8.6に変更したものの、同様のエラーが発生してしまいます。

- 「コマンドを実行した」のは EC2ホスト or Dockerコンテナ内部 ? ⇒ ECホスト
- Webアプリが実行されているのは EC2ホスト or Dockerコンテナ内部 ? ⇒ Dockerコンテナ
  - ⇒「pip install」に意味がない
  - ⇒Dockerコンテナの再ビルドが必要。

※"ホスト" というのは、Docker自体を起動している環境のこと

### ①

- Beforeの確認

コンテナ環境にログインして、ライブラリのバージョン確認をする

```shell
$ # コンテナ状態確認
$ docker-compose ps
      Name                    Command               State                      Ports                    
--------------------------------------------------------------------------------------------------------
dss_docker_app_1   ./start-app.sh                   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp    
dss_docker_db_1    docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp,:::5432->5432/tcp    
dss_docker_web_1   /docker-entrypoint.sh ngin ...   Up      80/tcp, 0.0.0.0:80->8080/tcp,:::80->8080/tcp

$ # app コンテナにログイン
$ docker-compose exec app bash

$ # Pythonライブラリを確認
pip3 freeze
```

- requirements.txt の修正

```diff
- psycopg2-binary
+ psycopg2-binary==2.8.*
```

- コンテナ再ビルド&起動

```shell
$ # ビルド
$ docker-compose build app

$ # 起動
$ docker-compose up -d

$ # ログ出力を確認
$ docker-compose logs app
```

## ②

> ubuntu@ip-172-31-38-33:~/dss_docker$ python3 manage.py createsuperuser

上記のコマンドがホスト側で実行されているため。コンテナ内部に入って実行しなければいけない。

```shell
$ # コンテナにログイン
$ docker-compose exec app bash

$ # createsuperuser を実行
python3 manage.py createsuperuser
...
```

# 仮想環境ことはじめ

- アプリケーション毎で使用するPythonライブラリは毎回同じとは限らない
  - ライブラリを使い分けたい
  - ⇒**仮想環境を使う**
- 同じアプリケーションなら、それらのバージョンは環境ごとで変わってほしくない。
  - ⇒使用する全てのライブラリバージョンを固定化したい

- requirements.txt は「使用したいライブラリを列挙するだけ」の役割
  - ⇒使用する**全ての**ライブラリのバージョンを固定する仕組みが必要

Pipenv or Poetry がおすすめ(これからは poetry が主流?)
※pyenv(Python自体のバージョン管理) + pipenv(ライブラリのバージョン管理)
