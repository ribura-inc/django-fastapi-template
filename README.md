# django-fastapi-template

Django x FastAPI template.

## プロジェクト概要📝

### Docker

Dockerを使用して開発環境を構築しています。そのため、各自の環境で用意しなければならないツールは最小限に抑えています。また、各自の環境が汚染されることも少なくなるようにしてあります。基本的には、Docker内にすべて閉じ込めています。（プロジェクト内に `.venv` は作成されます。）

### Pythonパッケージ管理ツール

Python用のパッケージ管理ツールは `Rye` を使用しています。

### Python fomatter/linter

Python用のfomatter/linterは `Ruff` を使用しています。

## セットアップ🛠️

1. リポジトリをクローン
2. pre-commitのセットアップ
    - 事前に各自でpre-commitをインストールしておくこと

    ```bash
    pre-commit install
    ```

3. envファイルの作成
   1. backend.env.sample をコピーして backend.env を作成

4. コンテナの起動

   1. rootに移動
   2. `rye sync` を実行c
   3. `docker compose up -d` を実行

5. マイグレーションの実行

   1. `docker compose exec backend bash` でコンテナに入る
   2. `python manage.py migrate` を実行

6. 管理者アカウントの作成

   1. `docker compose exec backend bash` でコンテナに入る
   2. `python manage.py createsuperuser` を実行
   3. ユーザー名、メールアドレス、パスワードを入力

7. 静的ファイルのコピー

   1. `docker compose exec backend bash` でコンテナに入る
   2. `python manage.py collectstatic` を実行
